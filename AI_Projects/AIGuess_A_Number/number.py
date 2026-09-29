import random

class GuessANumber:
    def __init__(self):
        self.lower_bound = 1
        self.upper_bound = 100
        self.guesses = 0
        self.difficulty_levels = {
            'easy': 1,
            'medium': 50,
            'hard': 100
        }

    def get_feedback(self, guess):
        print(f"Is your number {guess}?")
        feedback = input("Enter 'h' if your number is higher, 'l' if it's lower, or 'c' if I'm correct: ")
        return feedback

    def guess(self):
        difficulty = input("Choose a difficulty level: easy (1-50), medium (1-75), or hard (1-100): ")
        if difficulty == 'easy':
            self.upper_bound = 50
        elif difficulty == 'medium':
            self.upper_bound = 75
        elif difficulty == 'hard':
            self.upper_bound = 100
        else:
            print("Invalid difficulty level. Defaulting to hard.")
            self.upper_bound = 100

        print(f"Think of a number between 1 and {self.upper_bound}.")
        while True:
            guess = (self.lower_bound + self.upper_bound) // 2
            feedback = self.get_feedback(guess)
            self.guesses += 1
            if feedback == 'h':
                self.lower_bound = guess + 1
            elif feedback == 'l':
                self.upper_bound = guess - 1
            elif feedback == 'c':
                print(f"Yay! I guessed your number in {self.guesses} guesses.")
                break
            else:
                print("Invalid feedback. Please enter 'h', 'l', or 'c'.")

    def play_again(self):
        play_again = input("Would you like to play again? (yes/no): ")
        if play_again.lower() == 'yes':
            self.lower_bound = 1
            self.upper_bound = 100
            self.guesses = 0
            self.guess()
            self.play_again()
        else:
            print("Thanks for playing!")

def main():
    game = GuessANumber()
    game.guess()
    game.play_again()

if __name__ == "__main__":
    main()