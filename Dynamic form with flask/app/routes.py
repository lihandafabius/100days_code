from flask import render_template, url_for, flash, redirect, session, request, jsonify, current_app
from app import db, bcrypt
from app.models import User, Product, CartItem
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import stripe

# Stripe setup
stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

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
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route("/add_to_cart/<int:product_id>", methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
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
    return render_template('checkout.html', total_price=total_price)


@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),  # Stripe requires the amount in cents
            },
            'quantity': item.quantity,
        })

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=url_for('success', _external=True),
        cancel_url=url_for('cancel', _external=True),
    )

    return jsonify({'id': checkout_session.id})


@app.route('/success')
def success():
    # Optionally clear the cart or implement order confirmation logic
    return render_template('success.html')


@app.route('/cancel')
def cancel():
    return render_template('cancel.html')


# About and Contact pages
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')
