from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from myapp import db, bcrypt
from myapp.forms import RegistrationForm, LoginForm, ProductForm, CommentForm
from myapp.models import User, Product, CartItem, ContactMessage
from functools import wraps
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import stripe
import bleach

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@main.route("/")
@main.route("/home")
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data, username=form.username.data, email=form.email.data,
                    password=hashed_password, is_admin=False)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully!', 'success')
        return redirect(url_for('main.login'))
    return render_template('registration.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['user'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('main.login'))

@main.route("/post_product", methods=["GET", "POST"])
@login_required
@admin_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product_name = form.product_name.data
        product_price = form.product_price.data

        product_description = bleach.clean(form.product_description.data, tags=[], strip=True)

        if form.product_image.data:
            image_file = secure_filename(form.product_image.data.filename)
            form.product_image.data.save(os.path.join('static/images', image_file))

        new_product = Product(name=product_name, price=product_price, description=product_description, image=image_file)
        db.session.add(new_product)
        db.session.commit()

        flash(f'Product {product_name} posted successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('post.html', form=form)

# Include the remaining routes similarly...
