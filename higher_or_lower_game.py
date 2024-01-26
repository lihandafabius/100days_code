from art6 import logo, vs
from random import choice
from higher_or_lower_game_data import data


def get_random_choices():
    # Choose two distinct random items from the data list
    choiceA = choice(data)
    choiceB = choice(data)

    # Make sure the choices are different
    while choiceA == choiceB:
        choiceB = choice(data)

    return choiceA, choiceB


def compare(comparison1, comparison2):
    if comparison1['follower_count'] > comparison2['follower_count']:
        return 'A'
    else:
        return 'B'


def print_score(points):
    print(f"Your current score is: {points}")


print(logo)

score = 0
choiceA, choiceB = get_random_choices()
while True:
    print(f"Compare A: {choiceA['name']}, a {choiceA['description']}, from {choiceA['country']}.")
    print(vs)
    print(f"Against B: {choiceB['name']}, a {choiceB['description']}, from {choiceB['country']}.")

    answer = input("Who has more followers? Type 'A' or 'B' (or 'Q' to quit): ")

    if answer.lower() == 'q':
        break  # Exit the loop if the user chooses to quit

    winner = compare(choiceA, choiceB)

    if answer.upper() == winner:
        score += 1
        print("Correct!")
    else:
        print("Wrong! Game over.")
        break  # Exit the loop if the user makes a wrong guess

    print_score(score)

    # Update choices for the next round
    choiceA, choiceB = choiceB, get_random_choices()[1]
