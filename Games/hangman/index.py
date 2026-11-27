import random
from collections.abc import Sequence

HANGMANPICS = [
"  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
"  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
"  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
"  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
"  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
"  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
"  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
]

CATEGORIES = {
    "1": ("Animals", "ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra".split()),
    "2": ("Fruits", "apple banana mango orange grape strawberry pineapple watermelon papaya kiwi lemon peach pear plum cherry blueberry coconut guava fig melon".split()),
    "3": ("Countries", "india japan france brazil canada germany italy spain egypt kenya mexico australia china russia turkey nepal thailand vietnam korea poland greece".split()),
    "4": ("Tech", "python java computer keyboard mouse monitor internet software hardware database server cloud robot code laptop".split()),
    "5": ("Harry Potter", "harry hermione ron dumbledore hogwarts gryffindor slytherin hagrid snape voldemort quidditch wand potion muggle azkaban dobby".split()),
}

DIFFICULTY = {
    "1": ("Easy", 8),
    "2": ("Medium", 6),
    "3": ("Hard", 4),
}

def get_random_word(word_list: Sequence[str]) -> str:
    return random.choice(word_list)

def display_board(
    missed_letters: str,
    correct_letters: str,
    secret_word: str,
    max_misses: int,
    hints_left: int,
    score: int,
    category_name: str,
) -> None:
    pic_index = min(len(missed_letters), len(HANGMANPICS) - 1)
    print(HANGMANPICS[pic_index])
    print()
    print(f"Category: {category_name} | Score: {score} | Hints left: {hints_left} | Misses: {len(missed_letters)}/{max_misses}")
    print('Missed letters:', end=' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print("\n")
    blanks = '_' * len(secret_word)
    for i in range(len(secret_word)):
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]
    for letter in blanks:
        print(letter, end=' ')
    print("\n")

def get_guess(already_guessed: str) -> str:
    while True:
        print("Guess a letter, or type 'hint' for a hint.")
        guess = input(">> ").lower().strip()
        if guess == "hint":
            return "hint"
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def use_hint(secret_word: str, correct_letters: str, hints_left: int) -> tuple[str, int]:
    if hints_left <= 0:
        print("No hints left!")
        return correct_letters, hints_left
    unguessed = [ch for ch in secret_word if ch not in correct_letters]
    if not unguessed:
        return correct_letters, hints_left
    revealed = random.choice(unguessed)
    print(f"Hint: the word contains '{revealed}'")
    return correct_letters + revealed, hints_left - 1

def choose_category():
    print("\nChoose a category:")
    for key, (name, _) in CATEGORIES.items():
        print(f"  {key}. {name}")
    while True:
        choice = input(">> pick 1-5: ").strip()
        if choice in CATEGORIES:
            return CATEGORIES[choice]
        print("Pick 1, 2, 3, 4 or 5.")

def choose_difficulty():
    print("\nChoose difficulty:")
    for key, (name, lives) in DIFFICULTY.items():
        print(f"  {key}. {name} ({lives} misses allowed)")
    while True:
        choice = input(">> pick 1-3: ").strip()
        if choice in DIFFICULTY:
            return DIFFICULTY[choice]
        print("Pick 1, 2 or 3.")

def play_round(score: int, wins: int, losses: int) -> tuple[int, int, int]:
    category_name, word_list = choose_category()
    diff_name, max_misses = choose_difficulty()
    secret_word = get_random_word(word_list)
    missed_letters = ''
    correct_letters = ''
    hints_left = 2
    print(f"\n--- {category_name} | {diff_name} | Word has {len(secret_word)} letters ---")
    while True:
        display_board(missed_letters, correct_letters, secret_word, max_misses, hints_left, score, category_name)
        guess = get_guess(missed_letters + correct_letters)
        if guess == "hint":
            correct_letters, hints_left = use_hint(secret_word, correct_letters, hints_left)
            if all(ch in correct_letters for ch in secret_word):
                print(f'Yes! The secret word is "{secret_word}"! You have won!')
                return score + 10, wins + 1, losses
            continue
        if guess in secret_word:
            correct_letters += guess
            if all(ch in correct_letters for ch in secret_word):
                display_board(missed_letters, correct_letters, secret_word, max_misses, hints_left, score, category_name)
                print(f'Yes! The secret word is "{secret_word}"! You have won!')
                return score + 10, wins + 1, losses
        else:
            missed_letters += guess
            if len(missed_letters) >= max_misses:
                display_board(missed_letters, correct_letters, secret_word, max_misses, hints_left, score, category_name)
                print(f"You have run out of guesses!\nAfter {len(missed_letters)} missed guesses and {len(correct_letters)} correct guesses, the word was \"{secret_word}\"")
                return score, wins, losses + 1

def play_again():
    print('Do you want to play again? (yes or no)')
    return input(">> ").lower().strip().startswith('y')

def main():
    print('H A N G M A N  -  UPGRADED')
    print("=" * 32)
    score = 0
    wins = 0
    losses = 0
    while True:
        score, wins, losses = play_round(score, wins, losses)
        print(f"\nScore: {score} | Wins: {wins} | Losses: {losses}")
        if not play_again():
            break
    print(f"\nFinal - Score: {score} | Wins: {wins} | Losses: {losses}")
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
