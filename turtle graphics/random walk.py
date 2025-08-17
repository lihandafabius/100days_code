import turtle
from turtle import Turtle, Screen
from random import randint, choice
tim = Turtle()
turtle.colormode(255)
directions = [0, 90, 180, 270]
tim.pensize(10)
tim.speed("fastest")


def change_colour():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r, g, b


for _ in range(100):
    tim.color(change_colour())
    tim.forward(30)
    tim.setheading(choice(directions))

screen = Screen()
screen.exitonclick()