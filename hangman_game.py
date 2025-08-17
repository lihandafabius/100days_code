import random
from hangman_art import logo, stages
from hangman_words import word_list
from clear_console import clear
print(logo)
chosen_word = random.choice(word_list)
print(chosen_word)
word_length = len(chosen_word)
display = []
lives = 6
for letter in chosen_word:
    display.append("_")
print(display)
end_of_game = False
while not end_of_game:
    guess = input("Enter a letter: ").lower()
    clear()
    if guess in display:
        print("You've already guessed that letter.")
    for index in range(word_length):
        if chosen_word[index] == guess:
            display[index] = guess
    if guess not in chosen_word:
        print(f"You guessed {guess}, that's not in the word.You lose a life.")
        lives -= 1
        if lives == 0:
            end_of_game = True
            print("You lose.")
    print(display)
    if "_" not in display:
        end_of_game = True
        print("You won")
    print(stages[lives])
    print(lives)