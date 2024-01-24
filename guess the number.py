from art5 import logo
import random


def play_game(attempts):
    should_continue = True
    while should_continue and attempts > 0:
        print(f"You have {attempts} attempts remaining to Guess the number")
        attempt = int(input("Make a Guess: "))
        if attempt == number:
            should_continue = False
            print(f"You Got it, the answer was {number}")
        elif attempts == 1:
            print("You've run out of Guesses, You lose")
            should_continue = False
        else:
            attempts -= 1
            if attempt > number:
                print("Too High")
            else:
                print("Too Low")


print(logo)
print("Welcome to the Number Guessing Game!")
number = random.randint(1, 100)
print("I'm thinking of a number between 1 and 100.")
level = input("Choose a difficulty. Type 'easy' or 'hard': ")
if level.lower() == "easy":
    play_game(10)
elif level.lower() == "hard":
    play_game(5)
else:
    print("Invalid entry, please enter either 'easy' or 'hard'")
