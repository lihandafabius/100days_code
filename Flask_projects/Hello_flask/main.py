from flask import Flask

app = Flask(__name__)


def make_bold(function):
    def wrapper(*args, **kwargs):
        return f'<b>{function(*args, **kwargs)}</b>'
    return wrapper


def make_emphasis(function):
    def wrapper(*args, **kwargs):
        return f'<em>{function(*args, **kwargs)}</em>'
    return wrapper


def make_underline(function):
    def wrapper(*args, **kwargs):
        return f'<u>{function(*args, **kwargs)}</u>'
    return wrapper


@app.route("/")
@make_bold
@make_emphasis
@make_underline
def hello_world():
    return ('<h1 style="text-align: center">Hello, World!</h1>'
            '<p>This is a paragraph</P>'
            '<img src="https://www.zooplus.co.uk/magazine/wp-content/uploads/2021/01/striped-grey-kitten.jpg" width=200>')


@app.route("/bye")
def say_bye():
    return "bye"


@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"hello {name + '12'}!. you are {number} years old."


if __name__ == "__main__":
    app.run(debug=True)

