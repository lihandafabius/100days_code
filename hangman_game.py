import random
stages = ['''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
      |
      |
      |
      |
=========
''']
word_list = ["aardvark", "baboon", "camel"]
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
    for index in range(word_length):
        if chosen_word[index] == guess:
            display[index] = guess
    if guess not in chosen_word:
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