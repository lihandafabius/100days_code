from flask import render_template, url_for, flash, redirect, session
from app import app, db, bcrypt
from models import User
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

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
        # Hash the user's password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create a new user
        user = User(fullname=form.fullname.data, username=form.username.data, email=form.email.data, password=hashed_password, is_admin=False)
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

# Logout route
@app.route('/logout')
@login_required
def logout():
    # Log out user with Flask-Login
    logout_user()
    # Clear user session
    session.pop('user', None)
    flash('You have successfully logged out!', 'info')
    return redirect(url_for('login'))
