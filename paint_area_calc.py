# Write your code below this line 👇
import math


def paint_calc(height, width, cover):
    area = height * width
    no_of_cans = math.ceil(area / cover)  # round to the number of cans ahead
    print(f"You'll need {no_of_cans} cans of paint")


# Write your code above this line 👆
# Define a function called paint_calc() so the code below works.

# 🚨 Don't change the code below 👇
test_h = int(input("Enter height of wall(m): "))
test_w = int(input("Enter Width of wall (m): "))
coverage = 5
paint_calc(height=test_h, width=test_w, cover=coverage)
