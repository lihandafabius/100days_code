from replit import clear
from art2 import logo

print(logo)
print("Welcome to the secret auction program.")
others = "yes"
bidding_list = []
while others.lower() == 'yes':
    bidder = input("What is your name:")
    bid = int(input("What's your bid:$ "))
    bidding_list.append({bidder: bid})
    others = input("Are there any other bidders? Type 'Yes' or 'No'.")
    clear()
    if others.lower() != 'yes':
        if others.lower() == 'no':
            max_bid = 0
            winner = ""
            for bidder_info in bidding_list:
                for key in bidder_info:
                    if bidder_info[key] > max_bid:
                        max_bid = bidder_info[key]
                        winner = key
            print(f"The winner is {winner} with a bid of ${max_bid}")
        else:
            print("Invalid entry")




