MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}
profit = 0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


def resource_sufficiency(order_ingredients):
    is_enough = True
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"Sorry there is not enough {item}.")
            is_enough = False
    return is_enough


def process_coins():
    print("Please insert coins")
    total = int(input("How many Quarters: ")) * 0.25
    total += int(input("How many Dimes: ")) * 0.10
    total += int(input("How many Nickles: ")) * 0.05
    total += int(input("How many Pennies: git push"
                       "")) * 0.01
    return total


def is_transaction_successful(money_received, drink_cost):
    if money_received > drink_cost:
        change = round(money_received - drink_cost, 2)
        print(f"Here is your change ${change}")
        global profit
        profit += drink_cost
        return True
    else:
        print("Sorry that's not enough money. Money refunded.")
        return False


def make_coffee(drink_name, order_ingredients):
    """Deduct the required ingredients from the resources."""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your {drink_name} ☕️. Enjoy!")


should_continue = True
while should_continue:
    # TODO 1 = Prompt user by asking “ What would you like? (espresso/latte/cappuccino):
    coffee_type = input("What would you like? (espresso/latte/cappuccino): ")

    # TODO 2 = Turn off the Coffee Machine by entering “ off ” to the prompt
    if coffee_type.lower() == 'off':
        should_continue = False
    # TODO 3 = Print report
    elif coffee_type.lower() == 'report':
        print(f"water: {resources['water']}ml")
        print(f"milk: {resources['milk']}ml")
        print(f"coffee: {resources['coffee']}g")
        print(f"money: {profit}")
# TODO 4 = Check resources sufficient?
    else:
        drink = MENU[coffee_type]
        if resource_sufficiency(drink["ingredients"]):
            payment = process_coins()
            if is_transaction_successful(payment, drink["cost"]):
                make_coffee(coffee_type, drink["ingredients"])