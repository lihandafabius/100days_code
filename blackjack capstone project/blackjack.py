from art4 import logo
import random
print(logo)

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def deal_card():
    return random.choice(cards)


def calculate_score(user_list, computer_list):
    user_value = sum(user_list)
    if user_value == 21:
        user_value = 0
    if user_value > 21 and 11 in user_list:
        user_list.remove(11)
        user_list.append(1)
    computer_score = sum(computer_list)
    if computer_score == 21:
        computer_score = 0
    return user_value, computer_score


user_cards = []
computer_cards = []
i = 0
while i < 2:
    user_cards.append(deal_card())
    computer_cards.append(deal_card())
    i += 1
print(computer_cards)
print(user_cards)
user_score, dealer_score = calculate_score(user_cards, computer_cards)
if user_score == 0:
    print("You won")
else:
    print(f"you got {user_score}")
if dealer_score == 0:
    print("Dealer wins")
else:
    print(f"Dealer got {dealer_score}")

