import random
from PIL import Image

HANGMAN_PICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
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
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg']  # replace with your image file paths
words = ['word1', 'word2', 'word3']  # replace with your corresponding words

def display_image(image_path):
    image = Image.open(image_path)
    image.show()

def display_board(HANGMAN_PICS, missed_letters, correct_letters, secret_word):
    print(HANGMAN_PICS[len(missed_letters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secret_word)

    for i in range(len(secret_word)):  # replace blanks with correctly guessed letters
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i + 1:]

    for letter in blanks:  # show the secret word with spaces in between each letter
        print(letter, end=' ')
    print()

def get_guess(already_guessed):
    while True:
        guess = input('Guess a letter.').lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def play_again():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def play_game():
    index = random.randint(0, len(image_paths) - 1)
    image_path = image_paths[index]
    secret_word = words[index]
    display_image(image_path)
    missed_letters = ''
    correct_letters = ''
    game_is_done = False

    while True:
        display_board(HANGMAN_PICS, missed_letters, correct_letters, secret_word)

        # Let the player type in a letter.
        guess = get_guess(missed_letters + correct_letters)

        if guess in secret_word:
            correct_letters = correct_letters + guess

            # Check if the player has won
            found_all_letters = True
            for i in range(len(secret_word)):
                if secret_word[i] not in correct_letters:
                    found_all_letters = False
                    break
            if found_all_letters:
                print('Yes! The secret word is "' + secret_word + '"! You have won!')
                if play_again():
                    index = random.randint(0, len(image_paths) - 1)
                    image_path = image_paths[index]
                    secret_word = words[index]
                    display_image(image_path)
                    missed_letters = ''
                    correct_letters = ''
                    game_is_done = False
                else:
                    break
        else:
            missed_letters = missed_letters + guess

            # Check if player has guessed too many times and lost
            if len(missed_letters) == len(HANGMAN_PICS) - 1:
                display_board(HANGMAN_PICS, missed_letters, correct_letters, secret_word)
                print('You have run out of guesses!\nAfter ' + str(len(missed_letters)) + ' missed guesses and ' + str(len(correct_letters)) + ' correct guesses, the word was "' + secret_word + '"')
                if play_again():
                    index = random.randint(0, len(image_paths) - 1)
                    image_path = image_paths[index]
                    secret_word = words[index]
                    display_image(image_path)
                    missed_letters = ''
                    correct_letters = ''
                    game_is_done = False
                else:
                    break

play_game()