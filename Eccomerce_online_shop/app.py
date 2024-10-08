from functools import wraps
import os

from django.core import mail
from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from flask_migrate import Migrate
from flask_wtf.file import FileAllowed
from wtforms.fields.choices import SelectField

from config import Config
import stripe
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor
from wtforms import IntegerField
from flask import g
from flask_mail import Mail, Message

import bleach

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate()

# Create the app
def create_app():
    app = Flask(__name__)
    ckeditor = CKEditor(app)
    app.config.from_object(Config)

    # Initialize the extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Stripe setup
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    with app.app_context():
        db.create_all()

    @app.context_processor
    def cart_item_count():
        if current_user.is_authenticated:
            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
            cart_item_count = sum(item.quantity for item in cart_items)
        else:
            cart_item_count = 0
        return dict(cart_item_count=cart_item_count)

    @app.before_request
    def check_maintenance_mode():
        # Get current settings from the database
        settings = Settings.get_settings()

        # Store settings globally for access in templates
        g.settings = settings

        # If maintenance mode is enabled and the user is not an admin, show the maintenance page
        if settings.maintenance_mode and (not current_user.is_authenticated or not current_user.is_admin):
            return render_template('maintenance.html'), 503  # 503 Service Unavailable

    # Routes
    @app.route("/")
    @app.route("/home")
    def home():
        products = Products.query.all()  # Query the database for all products
        return render_template('index.html', products=products, settings=settings)
    @app.before_request
    def load_settings():
        settings = Settings.get_settings()
        g.settings = settings  # Use Flask's global object `g` to pass settings

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(fullname=form.fullname.data, username=form.username.data, email=form.email.data,
                        phone=form.phone.data,
                        password=hashed_password, is_admin=False)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created successfully!', 'success')
            return redirect(url_for('login'))
        return render_template('registration.html', title='Register', form=form)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session['user'] = user.id  # Save user session with ID
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html', title='Login', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.pop('user', None)
        session['logout_flash'] = "Successfully logged out!"
        return redirect(url_for('login'))

    # Admin required decorator (example)
    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_admin:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)

        return decorated_function

    @app.route("/post_product", methods=["GET", "POST"])
    @login_required
    @admin_required
    def add_product():
        form = ProductForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            product_price = form.product_price.data
            product_category = form.product_category.data  # Add category
            product_stock = form.product_stock.data  # Add stock

            # Strip HTML tags from the description to prevent storing HTML
            product_description = bleach.clean(form.product_description.data, tags=[], strip=True)

            # Save image
            image_file = 'default.jpg'  # Default image
            if form.product_image.data:
                image_file = secure_filename(form.product_image.data.filename)
                form.product_image.data.save(os.path.join(app.root_path, 'static/images', image_file))

            # Add product to database
            new_product = Products(name=product_name, price=product_price, category=product_category,
                                   stock=product_stock, description=product_description, image=image_file)
            db.session.add(new_product)
            db.session.commit()

            flash(f'Product {product_name} posted successfully!', 'success')
            return redirect(url_for('home'))

        return render_template('post.html', form=form)

    @app.route("/product/edit/<int:product_id>", methods=['GET', 'POST'])
    @login_required
    @admin_required
    def edit_product(product_id):
        product = Products.query.get_or_404(product_id)
        form = ProductForm()

        if form.validate_on_submit():
            # Update product details
            product.name = form.product_name.data
            product.price = form.product_price.data
            product.category = form.product_category.data  # Update category
            product.stock = form.product_stock.data  # Update stock

            # Strip HTML tags from the description to prevent storing HTML
            product.description = bleach.clean(form.product_description.data, tags=[], strip=True)

            # Save the new image if uploaded
            if form.product_image.data:
                image_file = secure_filename(form.product_image.data.filename)
                form.product_image.data.save(os.path.join(app.root_path, 'static/images', image_file))
                product.image = image_file

            db.session.commit()
            flash(f'Product {product.name} updated successfully!', 'success')
            return redirect(url_for('home'))

        # Pre-fill the form with existing product data
        elif request.method == 'GET':
            form.product_name.data = product.name
            form.product_price.data = product.price
            form.product_category.data = product.category  # Pre-fill category
            form.product_stock.data = product.stock  # Pre-fill stock
            form.product_description.data = product.description

        return render_template('edit_product.html', form=form, product=product)

    @app.route("/product/delete/<int:product_id>", methods=['POST'])
    @login_required
    @admin_required
    def delete_product(product_id):
        product = Products.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash(f'Product {product.name} deleted successfully!', 'success')
        return redirect(url_for('home'))

    @app.route('/handle_flash')
    def handle_flash():
        if 'logout_flash' in session:
            flash(session['logout_flash'], 'success')
            session.pop('logout_flash')  # Remove the flash message after it's shown
        return redirect(url_for('login'))

    @app.route("/cart")
    @login_required
    def cart():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        cart_item_count = sum(item.quantity for item in cart_items)  # Count total items in the cart
        return render_template('cart.html', cart_items=cart_items, total_price=total_price,
                               cart_item_count=cart_item_count)

    @app.route("/add_to_cart/<int:product_id>", methods=['POST'])
    @login_required
    def add_to_cart(product_id):
        product = Products.query.get_or_404(product_id)  # Ensure product exists

        # Check if stock is available
        if product.stock > 0:
            existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

            if existing_item:
                existing_item.quantity += 1
            else:
                cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
                db.session.add(cart_item)

            # Decrease stock after item is added to the cart
            product.stock -= 1

            db.session.commit()
            flash(f'{product.name} added to cart!', 'success')
        else:
            flash(f'{product.name} is out of stock!', 'danger')

        return redirect(url_for('cart'))

    @app.route("/remove_from_cart/<int:cart_item_id>", methods=['POST'])
    @login_required
    def remove_from_cart(cart_item_id):
        cart_item = CartItem.query.get_or_404(cart_item_id)
        if cart_item.user_id != current_user.id:
            flash("You cannot remove this item", 'danger')
            return redirect(url_for('cart'))
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart!', 'success')
        return redirect(url_for('cart'))

    @app.route("/checkout")
    @login_required
    def checkout():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        line_items = [
            {
                'name': item.product.name,
                'description': item.product.description,
                'price': item.product.price,
                'quantity': item.quantity,
                'image_url': url_for('static', filename=f'images/{item.product.image}', _external=True)
            }
            for item in cart_items
        ]

        return render_template('checkout.html', line_items=line_items, total_price=total_price)

    @app.route('/create-checkout-session', methods=['POST'])
    @login_required
    def create_checkout_session():
        try:
            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

            if not cart_items:
                return jsonify({'error': 'Your cart is empty.'}), 400

            # Prepare line items for Stripe
            line_items = [
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.product.price * 100),
                    },
                    'quantity': item.quantity,
                }
                for item in cart_items
            ]

            # Create a Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=url_for('success', _external=True),
                cancel_url=url_for('cancel', _external=True),
            )

            # After payment is successful, create the order
            @app.route('/success')
            def success():
                order = Order(user_id=current_user.id,
                              total_price=sum(item.product.price * item.quantity for item in cart_items))
                db.session.add(order)
                db.session.commit()

                # Add each cart item as an OrderItem
                for item in cart_items:
                    order_item = OrderItem(order_id=order.id, product_id=item.product.id, quantity=item.quantity)
                    db.session.add(order_item)

                # Clear the cart after order creation
                CartItem.query.filter_by(user_id=current_user.id).delete()
                db.session.commit()

                return render_template('success.html', order=order)

            return jsonify({'id': checkout_session.id})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Dashboard route for admins
    @app.route('/dashboard')
    @login_required
    @admin_required
    def dashboard():
        # Fetch data to display on the dashboard
        products = Products.query.all()  # Fetch all products
        users = User.query.all()  # Fetch all users
        messages = ContactMessage.query.all()  # Fetch all contact form messages

        # Render the dashboard template, passing the fetched data
        return render_template('dashboard.html', products=products, users=users, messages=messages)

    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def settings():
        form = AdminForm()

        # Handle the form submission to add an admin
        if form.validate_on_submit():
            email = form.email.data
            user = User.query.filter_by(email=email).first()
            if user:
                if not user.is_admin:
                    user.is_admin = True
                    db.session.commit()
                    flash(f'{user.email} is now an admin!', 'success')
                else:
                    flash(f'{user.email} is already an admin.', 'warning')
            else:
                flash('No user found with that email.', 'danger')

        # Retrieve all admins from the database
        admins = User.query.filter_by(is_admin=True).all()

        return render_template('settings.html', form=form, admins=admins)

    # Route to remove admin privileges
    @app.route('/remove_admin/<int:admin_id>', methods=['POST'])
    @login_required
    @admin_required
    def remove_admin(admin_id):
        user = User.query.get_or_404(admin_id)

        if user.is_admin:
            user.is_admin = False
            db.session.commit()
            flash(f'{user.email} is no longer an admin.', 'success')
        else:
            flash(f'{user.email} is not an admin.', 'warning')

        return redirect(url_for('settings'))

    @app.route('/success')
    def success():
        return render_template('success.html')

    @app.route('/cancel')
    def cancel():
        return render_template('cancel.html')

    @app.route("/about")
    def about():
        return render_template('about.html', title='About')

    @app.route('/orders')
    @login_required
    @admin_required
    def orders():
        orders = Order.query.all()
        return render_template('orders.html', orders=orders)


    @app.route('/products')
    @login_required
    @admin_required
    def products():
        # Logic for displaying products
        # Query all products from the database
        products = Products.query.all()

        # Pass the products to the template
        return render_template('products.html', products=products)

    @app.route('/customers')
    @login_required
    @admin_required
    def customers():
        # Logic for displaying customers
        return render_template('customers.html')

    @app.route('/reports')
    @login_required
    @admin_required
    def reports():
        # Logic for displaying reports
        return render_template('reports.html')

    @app.route('/integrations')
    @login_required
    @admin_required
    def integrations():
        # Logic for displaying integrations
        return render_template('integrations.html')

    from flask import render_template, request
    import bleach

    @app.route("/contact", methods=['GET', 'POST'])
    def contact():
        msg_sent = False
        if request.method == 'POST':
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')

            # Clean message input using bleach, allowing specific HTML tags
            allowed_tags = ['b', 'i', 'u', 'strong', 'em', 'p', 'br']
            message = bleach.clean(request.form.get('message'), tags=allowed_tags, strip=True)

            # Save contact message to the database
            new_message = ContactMessage(name=name, email=email, phone=phone, message=message)
            db.session.add(new_message)
            db.session.commit()

            # Set success flag
            msg_sent = True

        return render_template('contact.html', msg_sent=msg_sent)

    @app.route('/update_contact_info', methods=['POST'])
    @login_required
    @admin_required
    def update_contact_info():
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        address = request.form.get('address')

        # Get the current settings (singleton pattern)
        settings = Settings.get_settings()

        # Update the contact information if provided
        if contact_email:
            settings.contact_email = contact_email
        if contact_phone:
            settings.contact_phone = contact_phone
        if address:
            settings.address = address

        # Commit changes to the database
        try:
            db.session.commit()
            flash('Contact information updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating contact information: {str(e)}', 'danger')

        return redirect(url_for('settings'))

    @app.route('/update_branding', methods=['POST'])
    @login_required
    @admin_required
    def update_branding():
        site_title = request.form.get('site_title')
        logo = request.files['site_logo']

        # Get the current settings (singleton pattern)
        settings = Settings.get_settings()

        # Update the site title if provided
        if site_title:
            settings.site_title = site_title

        # Handle file upload and save logic for the logo
        if logo:
            # Generate a secure filename
            filename = secure_filename(logo.filename)
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file in the defined upload folder
            logo.save(logo_path)

            # Save the filename in the database (you may store just the file name or relative path)
            settings.site_logo = filename

        # Commit changes to the database
        try:
            db.session.commit()
            flash('Branding updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating branding: {str(e)}', 'danger')

        return redirect(url_for('settings'))

    @app.route('/toggle_maintenance', methods=['POST'])
    @login_required
    @admin_required
    def toggle_maintenance():
        maintenance_mode = 'maintenance_mode' in request.form

        # Get the current settings
        settings = Settings.get_settings()

        # Update the maintenance mode in the database
        settings.maintenance_mode = maintenance_mode

        try:
            db.session.commit()
            flash('Maintenance mode updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating maintenance mode: {str(e)}', 'danger')

        return redirect(url_for('settings'))

    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        email = request.form.get('email')
        if email:
            # Check if already subscribed
            if Subscriber.query.filter_by(email=email).first():
                flash('You are already subscribed.', 'info')
            else:
                subscriber = Subscriber(email=email)
                db.session.add(subscriber)
                db.session.commit()
                flash('You have successfully subscribed!', 'success')
        else:
            flash('Please provide a valid email.', 'danger')
        return redirect(url_for('home'))

    @app.route('/send_newsletter', methods=['POST'])
    @login_required
    @admin_required
    def send_newsletter():
        content = request.form.get('content')
        subscribers = Subscriber.query.all()

        for subscriber in subscribers:
            msg = Message('New Stock Available!', recipients=[subscriber.email])
            msg.body = content
            mail.send(msg)

        flash('Notification sent to subscribers successfully!', 'success')
        return redirect(url_for('products'))

    return app

# Forms (RegistrationForm, LoginForm, CommentForm)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_ckeditor import CKEditorField

class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    comment_text = CKEditorField("Write your comment", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Admin')



class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_price = DecimalField('Price', validators=[DataRequired()])
    product_category = SelectField('Category', choices=[('men', 'Men'), ('women', 'Women'), ('kids', 'Kids'),
                                                        ('others', 'Others')], validators=[DataRequired()])
    product_stock = IntegerField('Stock', validators=[DataRequired()])
    product_image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png'])])
    product_description = CKEditorField('Description', validators=[DataRequired()])
    submit = SubmitField('Post Product')


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String(100), nullable=False, default="Bitbanta store")
    site_logo = db.Column(db.String(100), nullable=True)  # Store logo file path
    contact_email = db.Column(db.String(100), nullable=False, default="info@bitbanta.com")
    contact_phone = db.Column(db.String(20), nullable=False, default="123-456-7890")
    address = db.Column(db.Text, nullable=True, default="123 Main St, City, Country")
    maintenance_mode = db.Column(db.Boolean, default=False)
    notifications_new_orders = db.Column(db.Boolean, default=True)
    notifications_customer_inquiries = db.Column(db.Boolean, default=True)
    notifications_low_stock = db.Column(db.Boolean, default=True)

    @staticmethod
    def get_settings():
        # Singleton pattern to ensure only one settings record
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
            db.session.commit()
        return settings



# Models (User, Product, CartItem)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
    category = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    # Define the relationship to CartItem with a backref
    cart_items = db.relationship('CartItem', backref='product', lazy=True)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Corrected here
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', backref='cart_items')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Assuming you have a user table
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.id}, User {self.user_id}>"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<OrderItem {self.id}, Order {self.order_id}, Products {self.product_id}>"


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<Subscriber {self.email}>'




if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
