import turtle
from turtle import Turtle, Screen
from random import randint

tim = Turtle()
turtle.colormode(255)
tim.speed("fastest")
tim.shape("classic")


def change_colour():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    random_colours = (r, g, b)
    return random_colours


for _ in range(100):
    tim.color(change_colour())
    tim.circle(100)
    tim.right(5)

screen = Screen()
screen.exitonclick()
