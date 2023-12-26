rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

# Write your code below this line 👇
import random

user_choice = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors\n"))
computer_choice = random.choice([rock, paper, scissors])
if user_choice == 0:
    print(rock)
    print(f"Computer chose: {computer_choice}")
    if user_choice == computer_choice:
        print("It's a tie!")
    if user_choice == 0 and computer_choice == paper:
        print("You lost!")
    if user_choice == 0 and computer_choice == scissors:
        print("You won!")
elif user_choice == 1:
    print(paper)
    print(f"Computer chose: {computer_choice}")
    if user_choice == computer_choice:
        print("It's a tie!")
    if user_choice == 1 and computer_choice == scissors:
        print("You lost!")
    if user_choice == 1 and computer_choice == rock:
        print("You won!")
elif user_choice == 2:
    print(scissors)
    print(f"Computer chose: {computer_choice}")
    if user_choice == computer_choice:
        print("It's a tie!")
    if user_choice == 2 and computer_choice == rock:
        print("You lost!")
    if user_choice == 2 and computer_choice == paper:
        print("You won!")
else:
    print("Invalid choice. Please choose 0, 1 or 2.")
