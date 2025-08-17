from datetime import datetime
from flask_login import UserMixin
from To_Do_List import db


class User(UserMixin, db.Model):
    """User model with authentication and task relationship"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    """Task model with status tracking"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    starred = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'

    def to_dict(self):
        """Convert task to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date.isoformat(),
            'completed': self.completed,
            'starred': self.starred,
            'created_at': self.created_at.isoformat()
        }