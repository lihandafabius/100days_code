from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=["GET"])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all", methods=["GET"])
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


# Updating the price of a cafe based on a particular id:
# http://127.0.0.1:5000/update-price/CAFE_ID?new_price=£5.67
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe_to_update = db.get_or_404(Cafe, cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        # Just add the code after the jsonify method. 200 = Ok
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        # 404 = Resource not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404

## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe_to_close = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        if cafe_to_close:
            db.session.delete(cafe_to_close)
            db.session.commit()
            return jsonify(resopnse={"Success": "Successfully deleted."}), 200
        else:
            return jsonify(error={"error": "Sorry, cafe with that id was not found in the database."}), 404
    else:
        return jsonify(response={"Forbidden": "Sorry, that's not allowed, make sure you have the correct api_key."}), 403


def str_to_bool(arg_from_url):
    if arg_from_url in ['True', 'true', 'T', 't', 'Yes', 'yes', 'y', '1']:
        return True
    else:
        return False


@app.route("/add", methods=["GET", "POST"])
def add_a_cafe():
    if request.method == "POST":
        name = request.args.get("name")
        new_cafe = Cafe(
            name=name,
            map_url=request.args.get("map_url"),
            img_url=request.args.get("img_url"),
            location=request.args.get("location"),
            seats=request.args.get("seats"),
            has_toilet=str_to_bool(request.args.get("has_toilet")),
            has_wifi=str_to_bool(request.args.get("has_wifi")),
            has_sockets=str_to_bool(request.args.get("has_sockets")),
            can_take_calls=str_to_bool(request.args.get("can_take_calls")),
            coffee_price=request.args.get("coffee_price")
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})
    else:
        return jsonify(response={"message": "Use POST to add a new cafe."})


if __name__ == '__main__':
    app.run(debug=True)
