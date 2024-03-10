from flask import Flask, render_template
from datetime import datetime
import requests
app = Flask(__name__)


@app.route("/")
def home():
    current_year = datetime.now().year
    return render_template("index.html", year=current_year)


@app.route("/guess/<name>")
def predict_gender(name):
    parameter = {
        "name": name,
        "country_id": "KE"
    }
    agify_params = {
        "name": name,
    }
    response = requests.get("https://api.genderize.io", params=parameter)
    data = response.json()
    name = data["name"]
    gender = data["gender"]
    age_response = requests.get("https://api.agify.io", params=agify_params)
    agify_data = age_response.json()
    age = agify_data["age"]
    return render_template("guess.html", name=name, gender=gender, age=age)


@app.route("/blog/<num>")
def get_blog(num):
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)