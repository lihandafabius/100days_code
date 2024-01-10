# Password Generator Project
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
print("""                                                                                                                                                                                                     
                                                                                              88                                                                                                       
                                                                                              88                                                                          ,d                           
                                                                                              88                                                                          88                           
8b,dPPYba,  ,adPPYYba, ,adPPYba, ,adPPYba, 8b      db      d8  ,adPPYba,  8b,dPPYba,  ,adPPYb,88     ,adPPYb,d8  ,adPPYba, 8b,dPPYba,   ,adPPYba, 8b,dPPYba, ,adPPYYba, MM88MMM ,adPPYba,  8b,dPPYba,  
88P'    "8a ""     `Y8 I8[    "" I8[    "" `8b    d88b    d8' a8"     "8a 88P'   "Y8 a8"    `Y88    a8"    `Y88 a8P_____88 88P'   `"8a a8P_____88 88P'   "Y8 ""     `Y8   88   a8"     "8a 88P'   "Y8  
88       d8 ,adPPPPP88  `"Y8ba,   `"Y8ba,   `8b  d8'`8b  d8'  8b       d8 88         8b       88    8b       88 8PP""""""" 88       88 8PP""""""" 88         ,adPPPPP88   88   8b       d8 88          
88b,   ,a8" 88,    ,88 aa    ]8I aa    ]8I   `8bd8'  `8bd8'   "8a,   ,a8" 88         "8a,   ,d88    "8a,   ,d88 "8b,   ,aa 88       88 "8b,   ,aa 88         88,    ,88   88,  "8a,   ,a8" 88          
88`YbbdP"'  `"8bbdP"Y8 `"YbbdP"' `"YbbdP"'     YP      YP      `"YbbdP"'  88          `"8bbdP"Y8     `"YbbdP"Y8  `"Ybbd8"' 88       88  `"Ybbd8"' 88         `"8bbdP"Y8   "Y888 `"YbbdP"'  88          
88                                                                                                   aa,    ,88                                                                                        
88                                                                                                    "Y8bbdP"                                                                                         
""")
nr_letters= int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

# Eazy Level - Order not randomised:
# e.g. 4 letter, 2 symbol, 2 number = JduE&!91
generated_password = []
for letter in range(nr_letters):
    generated_password.append(random.choice(letters))
for symbol in range(nr_symbols):
    generated_password.append(random.choice(symbols))
for number in range(nr_numbers):
    generated_password.append(random.choice(numbers))
print(generated_password)
random.shuffle(generated_password)
print(generated_password)
password = ''.join(generated_password)
print(password)

# Hard Level - Order of characters randomised:
# e.g. 4 letter, 2 symbol, 2 number = g^2jk8&P
