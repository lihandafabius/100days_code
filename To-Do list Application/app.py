
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bootstrap import Bootstrap


app = Flask(__name__)

# Configure the application and database
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
Bootstrap(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)


# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    task_done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Flask-WTF forms
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=150)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=150)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    task = StringField('Task', validators=[InputRequired(), Length(max=200)])
    due_date = StringField('Due Date', validators=[InputRequired(), Length(max=100)])
    submit = SubmitField('Add Task')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def index():
    form = TaskForm()
    tasks = Task.query.filter_by(owner=current_user).all()
    return render_template('dashboard.html', form=form, tasks=tasks, user=current_user)


@app.route('/todo')
@login_required
def todo():
    form = TaskForm()  # If needed for the todo route
    tasks = Task.query.filter_by(owner=current_user).all()  # If needed for the todo route
    return render_template('dashboard.html', form=form, tasks=tasks, user=current_user)


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            task=form.task.data,
            due_date=form.due_date.data,
            task_done=False,
            owner=current_user
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_task.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(task=form.task.data, due_date=form.due_date.data, owner=current_user)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    tasks = Task.query.filter_by(owner=current_user).all()
    return render_template('dashboard.html', form=form, tasks=tasks, user=current_user)


@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to update this task.', 'danger')
        return redirect(url_for('dashboard'))
    form = TaskForm()
    if form.validate_on_submit():
        task.task = form.task.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.task.data = task.task
        form.due_date.data = task.due_date
    return render_template('update_task.html', form=form, task=task)  # Pass the task variable


@app.route('/update_task_status/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to update this task.', 'danger')
        return redirect(url_for('dashboard'))

    task.task_done = request.form.get('task_done') == 'on'
    db.session.commit()
    flash('Task status updated successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/tasks/<status>')
@login_required
def tasks(status):
    form = TaskForm()  # Create a dummy form object
    if status == 'finished':
        tasks = Task.query.filter_by(owner=current_user, task_done=True).all()
    elif status == 'unfinished':
        tasks = Task.query.filter_by(owner=current_user, task_done=False).all()
    else:
        flash('Invalid status parameter.', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('tasks.html', tasks=tasks, status=status, form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


