from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
import datetime as dt

from To_Do_List import db, login_manager
from To_Do_List.models import User, Task
from To_Do_List.forms import RegisterForm, LoginForm, TaskForm
from config import Config

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------------------- Auth Routes ---------------------

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.dashboard'))
        flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --------------------- Task Dashboard ---------------------

@main.route('/')
@login_required
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard', methods=['GET', 'POST'])
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

@main.route('/todo')
@login_required
def todo():
    form = TaskForm()
    tasks = Task.query.filter_by(owner=current_user).all()
    return render_template('dashboard.html', form=form, tasks=tasks, user=current_user)

@main.route('/add_task', methods=['GET', 'POST'])
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
        return redirect(url_for('main.dashboard'))
    return render_template('add_task.html', form=form)

# --------------------- Task Management ---------------------

@main.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to delete this task.', 'danger')
    else:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to update this task.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = TaskForm()
    if form.validate_on_submit():
        task.task = form.task.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.task.data = task.task
        form.due_date.data = task.due_date
    return render_template('update_task.html', form=form, task=task)

@main.route('/update_task_status/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to update this task.', 'danger')
    else:
        task.task_done = request.form.get('task_done') == 'on'
        db.session.commit()
        flash('Task status updated successfully.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/toggle_star/<int:task_id>', methods=['POST'])
@login_required
def toggle_star(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to star this task.', 'danger')
    else:
        task.starred = not task.starred
        db.session.commit()
        flash('Task star status updated successfully.', 'success')
    return redirect(url_for('main.dashboard'))

# --------------------- Task Filters ---------------------

@main.route('/tasks/<status>')
@login_required
def tasks(status):
    form = TaskForm()
    if status == 'finished':
        tasks = Task.query.filter_by(owner=current_user, task_done=True).all()
    elif status == 'unfinished':
        tasks = Task.query.filter_by(owner=current_user, task_done=False).all()
    else:
        flash('Invalid status parameter.', 'danger')
        return redirect(url_for('main.dashboard'))
    return render_template('tasks.html', tasks=tasks, status=status, form=form)

@main.route('/tasks/starred')
@login_required
def starred_tasks():
    form = TaskForm()
    tasks = Task.query.filter_by(owner=current_user, starred=True).all()
    return render_template('tasks.html', tasks=tasks, status='starred', form=form)

# --------------------- Email Reminder System ---------------------

def send_reminder_email(user, task):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=Config.MAIL_USERNAME, password=Config.MAIL_PASSWORD)
        message = f"Subject: Task Due Today\n\nDear {user.username},\n\nThis is a reminder that your task '{task.task}' is due today."
        connection.sendmail(
            from_addr=Config.MAIL_USERNAME,
            to_addrs=user.email,
            msg=message
        )

def check_due_tasks():
    today = dt.datetime.now().strftime("%Y-%m-%d")
    tasks_due_today = Task.query.filter_by(due_date=today, task_done=False).all()
    for task in tasks_due_today:
        send_reminder_email(task.owner, task)
