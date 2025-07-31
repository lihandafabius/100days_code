# weight = int(input("Weight: "))
# conversion = input("K(g) or L(b): ")
# if conversion.upper() == "K":
#     weight /= 10
#     print(weight)
# elif conversion.upper() == "L":
#     weight /= 0.220462
#     print(weight)
#
# else:
#     print("Please enter either 'k' or 'l'.")


# def number_type(number):
#
#     if number % 2 == 0:
#         print("Even")
#     else:
#         print("Odd")
# number = int(input("Enter number:"))
# number_type(number)


# numbers = [2,3,4,5,6]
# for number in numbers:
#     number *= number
#     print(number)
#

def ceaser_cipher(p_text, shift_amount, direction):
    result = ""
    for char in p_text:
        if char.isalpha():
            index = alphabet.index(char.lower())
            shifted_index = (index + shift_amount) % 26
            if direction == 'decode':
                shifted_index = (index - shift_amount) % 26
            shifted_char = alphabet[shifted_index]
            result += shifted_char
        else:
            result += char  # Keep non-alphabetic characters unchanged
    print(f"The {direction}d text is {result}")


repeat = 'yes'
while repeat.lower() == 'yes':
    direction = input("Type 'encode' to encrypt and 'decode' to decrypt: ")
    if direction == 'encode' or direction == 'decode':
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        text = input("Enter your message: \n")
        shift = int(input("Enter shift number: \n"))
        ceaser_cipher(p_text=text, shift_amount=shift, direction=direction)

    else:
        print("Invalid entry. Please type 'encode' or 'decode' to proceed.")
    repeat = input("Type 'yes' if you want to go again. Otherwise type 'no':\n")

if repeat.lower() != "yes":
    print("Goodbye")