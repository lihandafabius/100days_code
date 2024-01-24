from art4 import logo
import replit
import random

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def deal_card():
    return random.choice(cards)


def calculate_score(card_list):
    total_score = sum(card_list)
    if total_score == 21 and len(card_list) == 2:
        return 0  # Blackjack
    if 11 in card_list and total_score > 21:
        card_list.remove(11)
        card_list.append(1)
    return total_score


def compare(user_score, dealer_score):
    if user_score > 21 and dealer_score > 21:
        return "You went over. You lose 😤"

    if user_score == dealer_score:
        return "Draw 🙃"
    elif dealer_score == 0:
        return "Lose, opponent has Blackjack 😱"
    elif user_score == 0:
        return "Win with a Blackjack 😎"
    elif user_score > 21:
        return "You went over. You lose 😭"
    elif dealer_score > 21:
        return "Opponent went over. You win 😁"
    elif user_score > dealer_score:
        return "You win 😃"
    else:
        return "You lose 😤"


def play_game():
    print(logo)
    user_cards = []
    computer_cards = []
    is_game_over = False

    # Initial deal
    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())

    while not is_game_over:
        user_score = calculate_score(user_cards)
        dealer_score = calculate_score(computer_cards)

        print(f"user_cards are {user_cards} and the user_score is {user_score}")
        print(f"computer's first card is {computer_cards[0]} and the computer_score is {dealer_score}")

        if user_score == 0 or user_score > 21 or dealer_score == 0:
            is_game_over = True
        else:
            user_should_deal = input("Type 'y' to get another card and type 'n' to pass: ")
            if user_should_deal.lower() == 'y':
                user_cards.append(deal_card())
            else:
                is_game_over = True

    while dealer_score != 0 and dealer_score < 17:
        computer_cards.append(deal_card())
        dealer_score = calculate_score(computer_cards)

    print(f"   Your final hand: {user_cards}, final score: {user_score}")
    print(f"   Computer's final hand: {computer_cards}, final score: {dealer_score}")
    print(compare(user_score, dealer_score))


while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == "y":
    replit.clear()
    play_game()
