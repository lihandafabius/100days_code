# Input a Python list of student heights
student_heights = []
length = int(input("Enter length of students height list: "))
for height in range(0, length):
    heights = int(input("Enter students heights: "))
    student_heights.append(heights)
# 🚨 Don't change the code above 👆

# Write your code below this row 👇
sum_heights = 0
no_of_students = 0
for height in student_heights:
    sum_heights += height
for i in student_heights:
    if i in student_heights:
        no_of_students += 1
avg_height = round(sum_heights / no_of_students)
print(f"total height = {sum_heights}")
print(f"number of students = {no_of_students}")
print(f"average height = {avg_height}")