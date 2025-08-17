print("Thank you for choosing Python Pizza Deliveries!")
size = input() # What size pizza do you want? S, M, or L
add_pepperoni = input() # Do you want pepperoni? Y or N
extra_cheese = input() # Do you want extra cheese? Y or N
# 🚨 Don't change the code above 👆
# Write your code below this line 👇
pepperoni_price = 0
price = 0
cheese_price = 0
if size == 'S':
  price = 15
  if add_pepperoni == 'Y':
    pepperoni_price = price + 2
    if extra_cheese == 'Y':
      cheese_price = pepperoni_price + 1
    if extra_cheese == 'N':
      cheese_price = pepperoni_price
  if add_pepperoni == 'N':
    pepperoni_price = price
    if extra_cheese == 'Y':
      cheese_price = pepperoni_price + 1
    if extra_cheese == 'N':
      cheese_price = pepperoni_price
if size == 'M':
  price = 20
  if add_pepperoni == 'Y':
    pepperoni_price = price + 3
    if extra_cheese == 'Y':
      cheese_price = pepperoni_price + 1
    if extra_cheese == 'N':
      cheese_price = pepperoni_price
  if add_pepperoni == 'N':
    pepperoni_price = price
    if extra_cheese == 'Y':
      cheese_price = pepperoni_price + 1
    if extra_cheese == 'N':
      cheese_price = pepperoni_price
if size == 'L':
  price = 25
  if add_pepperoni == 'Y':
    pepperoni_price = price + 3
    if extra_cheese == 'Y':
      cheese_price = pepperoni_price + 1
    if extra_cheese == 'N':
      cheese_price = pepperoni_price
  if add_pepperoni == 'N':
    pepperoni_price = price
    if extra_cheese == 'Y':
      cheese_price = pepperoni_price + 1
    if extra_cheese == 'N':
      cheese_price = pepperoni_price
final_bill = price + pepperoni_price + cheese_price
print(f"Your final bill is: ${final_bill}")