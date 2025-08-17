from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap5


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Length(min=6, max=120, message='Little short for an email address?'), Email(message='That\'s not a valid email address.')])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, message='password must be atleast 8 characters long')])
    submit = SubmitField(label='Log in')


app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == 'admin@email.com' and login_form.password.data == "12345678":
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)