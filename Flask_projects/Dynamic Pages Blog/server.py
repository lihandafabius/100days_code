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
    response = requests.get("https://api.genderize.io", params=parameter)
    data = response.text
    print(data)
    return data


if __name__ == "__main__":
    app.run(debug=True)