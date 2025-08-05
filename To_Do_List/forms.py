from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from datetime import date

from To_Do_List.models import User

class BaseForm(FlaskForm):
    """Base form with common methods"""
    class Meta:
        csrf = True

    def validate_on_submit(self):
        """Add form-specific validation"""
        return super().validate_on_submit()

class RegisterForm(BaseForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=50)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=100)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=100)
    ])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class LoginForm(BaseForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class TaskForm(BaseForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=200)
    ])
    description = TextAreaField('Description', validators=[
        Length(max=500)
    ])
    due_date = DateField('Due Date', validators=[
        DataRequired()
    ], default=date.today)
    submit = SubmitField('Save Task')

    def validate_due_date(self, field):
        if field.data < date.today():
            raise ValidationError('Due date cannot be in the past.')