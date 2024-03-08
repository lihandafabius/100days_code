from flask import Flask

app = Flask(__name__)


@app.route("/")
def guess_a_number():
    return ('<h1>Guess a number between 0 and 9</h1>'
            '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnZub2NjMGs5ZnQ0aHpqN2YzZGd1MWR5NnZsNmQ0d3B5czllNmFqbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wIo1jZH4iHf6xRwJu4/giphy.gif">')


if __name__ == "__main__":
    app.run(debug=True)