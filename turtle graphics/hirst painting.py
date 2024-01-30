import turtle
from turtle import Turtle, Screen
import random

turtle.colormode(255)
tim = Turtle()
tim.speed("fastest")
tim.penup()
tim.hideturtle()

color_list = [(220, 219, 214), (14, 26, 61), (14, 39, 149), (50, 91, 154), (55, 24, 11), (224, 220, 222), (125, 157, 199),
 (52, 22, 34), (185, 176, 23), (210, 216, 226), (140, 25, 14), (133, 85, 46), (124, 76, 94), (79, 119, 194),
 (119, 32, 43), (186, 167, 119), (180, 143, 157), (213, 221, 215), (210, 201, 130), (14, 26, 19), (169, 102, 118),
 (168, 185, 224), (93, 80, 13), (220, 206, 11), (21, 77, 99), (82, 108, 95), (147, 171, 151), (74, 144, 172),
 (218, 173, 185), (165, 108, 100)]

tim.setheading(225)
tim.forward(300)
tim.setheading(0)
no_of_dots = 100
for dot_count in range(1, no_of_dots + 1):
    tim.dot(20, random.choice(color_list))
    tim.forward(50)
    if dot_count % 10 == 0:
        tim.setheading(90)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(500)
        tim.setheading(0)


screen = Screen()
screen.exitonclick()