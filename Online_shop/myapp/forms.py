from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_ckeditor import CKEditorField

class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    comment_text = CKEditorField("Write your comment", validators=[DataRequired()])
    submit = SubmitField("Submit")

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_price = DecimalField('Product Price', validators=[DataRequired()])
    product_image = FileField('Product Image', validators=[DataRequired()])
    product_description = CKEditorField('Product Description', validators=[DataRequired()])
