from art import logo
print(logo)


def ceaser(entry_text, shift_amount, cipher_direction):
    end_result = ""
    for char in entry_text:
        if char.isalpha():  # or if char in alphabet
            index = alphabet.index(char.lower())
            shifted_index = (index + shift_amount) % 26
            if cipher_direction == "decode":
                shifted_index = (index - shift_amount) % 26
            shifted_char = alphabet[shifted_index]
            end_result += shifted_char
        else:
            end_result += char  # Keep non-alphabetic characters unchanged
    print(f"The {cipher_direction}d text is {end_result}")


repeat = "yes"
while repeat.lower() == "yes":
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")

    if direction == "encode" or direction == "decode":
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']  # adhere to pep style
        text = input("Type your message:\n").lower()
        shift = int(input("Type the shift number:\n"))
        ceaser(entry_text=text, shift_amount=shift, cipher_direction=direction)
    else:
        print("Invalid entry. Please type 'encode' or 'decode' to proceed.")
    repeat = input("Type 'yes' if you want to go again. Otherwise type 'no':\n")

if repeat.lower() != "yes":
    print("Goodbye")


