print("Welcome to the tip calculator.")
bill = float(input("What was the total bill? $"))
tip_percentage = int(input("What percentage tip would you like to give? 10, 12, or 15? "))
if tip_percentage == 10:
    tip = bill * 0.1
    people = int(input("How many people to split the bill? "))
    pay = round(((bill + tip) / people), 2)
    print(f"Each person should pay: ${pay}")
if tip_percentage == 12:
    tip = bill * 0.12
    people = int(input("How many people to split the bill? "))
    pay = round(((bill + tip) / people), 2)
    print(f"Each person should pay: ${pay}")

if tip_percentage == 15:
    tip = bill * 0.15
    people = int(input("How many people to split the bill? "))
    pay = round(((bill + tip) / people), 2)
    print(f"Each person should pay: ${pay}")






