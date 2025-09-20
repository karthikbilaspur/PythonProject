import requests

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

def get_random_word():
    response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
    return response.json()[0]

def get_definition(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    try:
        data = response.json()[0]
        return data['meanings'][0]['definitions'][0]['definition']
    except:
        return "No definition found."

def displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord, definition):
    print(HANGMAN_PICS[len(missedLetters)])
    print(f"Hint: {definition}")
    print()

    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # replace blanks with correctly guessed letters
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # show the secret word with spaces in between each letter
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    # Returns the letter the player entered. This function makes sure the player entered a single letter, and not something else.
    while True:
        guess = input('Guess a letter.').lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def play_game():
    secretWord = get_random_word()
    definition = get_definition(secretWord)
    missedLetters = ''
    correctLetters = ''
    gameIsDone = False

    while True:
        displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord, definition)

        # Let the player type in a letter.
        guess = getGuess(missedLetters + correctLetters)

        if guess in secretWord:
            correctLetters = correctLetters + guess

            # Check if the player has won
            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print('Yes! The secret word is "' + secretWord + '"! You have won!')
                if playAgain():
                    secretWord = get_random_word()
                    definition = get_definition(secretWord)
                    missedLetters = ''
                    correctLetters = ''
                    gameIsDone = False
                else:
                    break
        else:
            missedLetters = missedLetters + guess

            # Check if player has guessed too many times and lost
            if len(missedLetters) == len(HANGMAN_PICS) - 1:
                displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord, definition)
                print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
                if playAgain():
                    secretWord = get_random_word = get_random_word()
                    definition = get_definition(secretWord)
                    missedLetters = ''
                    correctLetters = ''
                    gameIsDone = False
                else:
                    break

play_game()