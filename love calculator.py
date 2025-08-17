print("The Love Calculator is calculating your score...")
name1 = input() # What is your name?
name2 = input() # What is their name?
# 🚨 Don't change the code above 👆
# Write your code below this line 👇
times1 = 0
times2 =0

combination = (name1 + name2).upper()
for char in combination:
    if char in 'TRUE':
        times1 += 1
    if char in 'LOVE':
        times2 += 1
times3 = str(times1) + str(times2)
love_score = int(times3)
if love_score < 10 or love_score > 90:
    print(f"Your score is {love_score}, you go together like coke and mentos.")
if 40 <= love_score <= 50:
    print(f"Your score is {love_score}, you are alright together.")
else:
    print(f"Your score is {love_score}.")

