names = []
i = 0
while i < 5:
    entry = input("Enter a name: ")
    names.append(entry)
    i += 1
print(names)
# The code above converts the input into an array seperating
# each name in the input by a comma and space.
# 🚨 Don't change the code above 👆
import random
length = len(names)
selected_guy = names[random.randint(0, length-1)]
print(f"{selected_guy} is going to buy the meal today!")
