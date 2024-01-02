import random
word_list = ["aardvark", "baboon", "camel"]
chosen_word = random.choice(word_list)
print(chosen_word)
word_length = len(chosen_word)
display = []
for letter in chosen_word:
    display.append("_")
print(display)
end = False
while not end:
    guess = input("Enter a letter: ").lower()
    for index in range(word_length):
        if chosen_word[index] == guess:
            display[index] = guess
    print(display)
    if "_" not in display:
        end = True
        print("You won")


