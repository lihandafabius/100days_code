import turtle
from turtle import Turtle, Screen
from random import randrange

tim = Turtle()
tim.shape("turtle")
tim.color("green")
turtle.colormode(255)


def change_colour():
    paint = randrange(0, 256)

    return paint


for sides in range(3,11):
    tim.color(change_colour(), change_colour(), change_colour())
    for _ in range(sides):
        tim.forward(100)
        tim.right(360 / sides)

screen = Screen()
screen.exitonclick()

