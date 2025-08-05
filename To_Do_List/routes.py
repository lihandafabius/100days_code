from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from To_Do_List import db, login_manager
from To_Do_List.models import User, Task
from To_Do_List.forms import RegisterForm, LoginForm, TaskForm
from To_Do_List.utils import send_reminder_email
from config import Config

main = Blueprint('main', __name__)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))

# --------------------- Auth Routes ---------------------
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data)
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

# --------------------- Task Dashboard ---------------------
@main.route('/')
@login_required
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    today = datetime.now().date()
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(
        Task.starred.desc(),
        Task.due_date.asc()
    ).all()
    return render_template('dashboard.html', tasks=tasks, today=today, user=current_user)

# --------------------- Task Management ---------------------
@main.route('/task/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        try:
            task = Task(
                title=form.title.data,
                due_date=form.due_date.data,
                user_id=current_user.id
            )
            db.session.add(task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add task. Please try again.', 'danger')
    return render_template('add_task.html', form=form)

@main.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = TaskForm(obj=task)
    if form.validate_on_submit():
        try:
            task.title = form.title.data
            task.due_date = form.due_date.data
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update task. Please try again.', 'danger')
    return render_template('edit_task.html', form=form, task=task)

@main.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to delete this task.', 'danger')
    else:
        try:
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to delete task. Please try again.', 'danger')
    return redirect(url_for('main.dashboard'))

@main.route('/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to modify this task.', 'danger')
    else:
        try:
            task.completed = not task.completed
            db.session.commit()
            status = 'completed' if task.completed else 'pending'
            flash(f'Task marked as {status}.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to update task status. Please try again.', 'danger')
    return redirect(url_for('main.dashboard'))


@main.route('/task/<int:task_id>/star', methods=['POST'])
@login_required
def toggle_star(task_id):
    """Toggle task star status"""
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You do not have permission to modify this task.', 'danger')
    else:
        try:
            task.starred = not task.starred
            db.session.commit()
            status = 'starred' if task.starred else 'unstarred'
            flash(f'Task {status}.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to update task. Please try again.', 'danger')
    return redirect(url_for('main.dashboard'))

# --------------------- Task Filters ---------------------
@main.route('/tasks/filter/<status>')
@login_required
def filter_tasks(status):
    valid_statuses = ['finished', 'unfinished']
    if status not in valid_statuses:
        flash('Invalid status parameter.', 'danger')
        return redirect(url_for('main.dashboard'))

    today = datetime.now().date()
    tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=(status == 'finished')
    ).order_by(
        Task.starred.desc(),
        Task.due_date.asc()
    ).all()
    return render_template('dashboard.html', tasks=tasks, today=today)

@main.route('/tasks/starred')
@login_required
def starred_tasks():
    today = datetime.now().date()
    tasks = Task.query.filter_by(
        user_id=current_user.id,
        starred=True
    ).order_by(
        Task.due_date.asc()
    ).all()
    return render_template('dashboard.html', tasks=tasks, today=today)

# --------------------- Email Reminder System ---------------------
def check_due_tasks():
    with scheduler.app.app_context():
        today = datetime.now().date()
        tasks = Task.query.filter_by(
            due_date=today,
            completed=False
        ).all()
        for task in tasks:
            try:
                send_reminder_email(task.owner, task)
            except Exception as e:
                current_app.logger.error(f"Failed to send reminder for task {task.id}: {e}")

scheduler.add_job(
    func=check_due_tasks,
    trigger='cron',
    hour=9,
    timezone='UTC'
)