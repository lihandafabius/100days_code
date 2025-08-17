import functools

from flask import Flask
import random

app = Flask(__name__)
number = random.randrange(0, 9)
print(number)
colours = ["red", "green", "orange", "yellow", "purple", "blue"]


def change_text_colour(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        color = random.choice(colours)
        original_response = func(*args, **kwargs)
        style_tag = f'<style>h1 {{color: {color};}}</style>'
        return style_tag + original_response
    return wrapper


def make_bold(function):
    def wrapper(*args, **kwargs):
        return f'<b>{function(*args, **kwargs)}</b>'
    return wrapper


@app.route("/")
@make_bold
def guess_a_number():
    return ('<h1>Guess a number between 0 and 9</h1>'
            '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">')


@app.route("/<int:input_number>")
@change_text_colour
def number_check(input_number):
    if input_number < number:
        return ('<h1>Too Low, Try Again!</h1>'
                '<img src = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnZub2NjMGs5ZnQ0aHpqN2YzZGd1MWR5NnZsNmQ0d3B5czllNmFqbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wIo1jZH4iHf6xRwJu4/giphy.gif">')

    elif input_number > number:
        return ('<h1>Too High, Try Again!</h1>'
                '<img src = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjRjZnJ5cmM2eXVwdjIxNTZ6YW53MmVocW54ZXBvczNzemlta2E3cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/u4aSP6BqkxhZiFHpdq/giphy.gif">')

    else:
        return ('<h1>You found me</h1>'
                '<img src = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjg4bHR4NTJudjUzMnF1MWpncWJjY3psb25qejZkN3JoNXl1djRmYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Q81NcsY6YxK7jxnr4v/giphy.gif">')


if __name__ == "__main__":
    app.run(debug=True)

