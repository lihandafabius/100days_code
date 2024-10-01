from functools import wraps
import os
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

    # Routes
    @app.route("/")
    @app.route("/home")
    def home():
        products = Products.query.all()  # Query the database for all products
        return render_template('index.html', products=products)

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(fullname=form.fullname.data, username=form.username.data, email=form.email.data,
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
        product = Products.query.get_or_404(product_id)

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
            # Fetch the cart items for the current user
            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

            # If no items in the cart, return an error
            if not cart_items:
                return jsonify({'error': 'Your cart is empty.'}), 400

            # Prepare line items for Stripe checkout session
            line_items = [
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.product.price * 100),  # Stripe accepts amounts in cents
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

            # Return the session ID to the frontend
            return jsonify({'id': checkout_session.id})

        except Exception as e:
            # Handle any errors that occur
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
    @login_required  # If the user must be logged in to view orders
    def orders():
        # Add logic for retrieving orders and rendering the orders page
        return render_template('orders.html')

    @app.route('/products')
    @login_required
    def products():
        # Logic for displaying products
        # Query all products from the database
        products = Products.query.all()

        # Pass the products to the template
        return render_template('products.html', products=products)

    @app.route('/customers')
    @login_required
    def customers():
        # Logic for displaying customers
        return render_template('customers.html')

    @app.route('/reports')
    @login_required
    def reports():
        # Logic for displaying reports
        return render_template('reports.html')

    @app.route('/integrations')
    @login_required
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


# Models (User, Product, CartItem)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
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



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
