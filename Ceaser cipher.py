def encrypt(plain_text, shift_amount):
    encoded_result = ""
    for char in text:
        if char.isalpha():
            index = alphabet.index(char.lower())
            shifted_index = (index + shift) % 26
            shifted_char = alphabet[shifted_index]
            encoded_result += shifted_char
        else:
            encoded_result += char  # Keep non-alphabetic characters unchanged

    print(f"The encoded text is {encoded_result}")


def decrypt(cypher_text, shift_amount):
    decoded_result = ""
    for char in text:
        if char.isalpha():
            index = alphabet.index(char.lower())
            shifted_index = (index - shift) % 26
            shifted_char = alphabet[shifted_index]
            decoded_result += shifted_char
        else:
            decoded_result += char  # Keep non-alphabetic characters unchanged
    print(f"The decoded text is {decoded_result}")


direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")

if direction == "encode" or direction == "decode":
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))

    if direction == "encode":
        encrypt(text, shift)
    else:
        decrypt(text, shift)
else:
    print("Invalid entry. Please type 'encode' or 'decode' to proceed.")

