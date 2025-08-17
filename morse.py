from MORSE_art import logo
print(logo)

# Morse code dictionary
morse_code_dict = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.',
    'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
    'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
    'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..', '0': '-----',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.', ' ': '/', '.': '.-.-.-', ',': '--..--',
    '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
}

# Reverse Morse code dictionary for decoding
reverse_morse_code_dict = {value: key for key, value in morse_code_dict.items()}


def morse_converter(entry_text, cipher_direction):
    if cipher_direction == "encode":
        return ' '.join(morse_code_dict[char] for char in entry_text.lower() if char in morse_code_dict)
    elif cipher_direction == "decode":
        return ''.join(reverse_morse_code_dict[char] for char in entry_text.split(' ') if char in reverse_morse_code_dict)


repeat = "yes"
while repeat.lower() == "yes":
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")

    if direction == "encode" or direction == "decode":
        text = input("Type your message to convert: \n").lower()
        result = morse_converter(entry_text=text, cipher_direction=direction)
        print(f"The {direction}d text is: {result}")
    else:
        print("Invalid entry. Please type 'encode' or 'decode' to proceed.")
    repeat = input("Type 'yes' if you want to go again. Otherwise type 'no':\n")

if repeat.lower() != "yes":
    print("Goodbye")
