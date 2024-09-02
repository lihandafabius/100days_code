from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
Bootstrap5(app)

# CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)

# CREATE TABLE


class Cafe(db.Model):
    name = db.Column(db.String(250), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(50), nullable=False)
    coffee_price = db.Column(db.String(50), nullable=False)


class AddCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets")
    has_toilet = BooleanField("Has Toilet")
    has_wifi = BooleanField("Has Wifi")
    can_take_calls = BooleanField("Can Take Calls")
    seats = StringField("Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Add Cafe")


@app.route("/")
def home():
    cafes = Cafe.query.all()
    return render_template("index.html", cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)


@app.route("/delete/<int:id>")
def delete_cafe(id):
    cafe_to_delete = Cafe.query.get_or_404(id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_cafe(id):
    cafe_to_edit = Cafe.query.get_or_404(id)
    form = AddCafeForm(
        name=cafe_to_edit.name,
        map_url=cafe_to_edit.map_url,
        img_url=cafe_to_edit.img_url,
        location=cafe_to_edit.location,
        has_sockets=cafe_to_edit.has_sockets,
        has_toilet=cafe_to_edit.has_toilet,
        has_wifi=cafe_to_edit.has_wifi,
        can_take_calls=cafe_to_edit.can_take_calls,
        seats=cafe_to_edit.seats,
        coffee_price=cafe_to_edit.coffee_price,
    )
    if form.validate_on_submit():
        cafe_to_edit.name=form.name.data
        cafe_to_edit.map_url = form.map_url.data
        cafe_to_edit.img_url = form.img_url.data
        cafe_to_edit.location = form.location.data
        cafe_to_edit.has_sockets = form.has_sockets.data
        cafe_to_edit.has_toilet = form.has_toilet.data
        cafe_to_edit.has_wifi = form.has_wifi.data
        cafe_to_edit.can_take_calls = form.can_take_calls.data
        cafe_to_edit.seats = form.seats.data
        cafe_to_edit.coffee_price = form.coffee_price.data

        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, cafe=cafe_to_edit)


if __name__ == '__main__':
    app.run(debug=True)
