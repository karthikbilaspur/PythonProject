import random

class CodeBreaker:
    def __init__(self):
        self.code = self.generate_code()
        self.guesses = 0

    def generate_code(self):
        # Generate a random 4-digit code
        return [random.randint(0, 9) for _ in range(4)]

    def get_feedback(self, guess):
        # Calculate feedback for the guess
        black_pegs = 0
        white_pegs = 0
        code_copy = self.code[:]
        guess_copy = guess[:]

        # Calculate black pegs (correct digit in correct position)
        for i in range(4):
            if guess_copy[i] == code_copy[i]:
                black_pegs += 1
                code_copy[i] = None
                guess_copy[i] = None

        # Calculate white pegs (correct digit in incorrect position)
        for i in range(4):
            if guess_copy[i] is not None and guess_copy[i] in code_copy:
                white_pegs += 1
                code_copy[code_copy.index(guess_copy[i])] = None
                guess_copy[i] = None

        return black_pegs, white_pegs

    def play(self):
        print("Welcome to Code Breaker!")
        print("I'm thinking of a 4-digit code.")
        print("You can guess the code by entering 4 digits.")

        while True:
            # Get user's guess
            user_guess = input("Enter your guess: ")
            if len(user_guess) != 4 or not user_guess.isdigit():
                print("Invalid guess. Please enter 4 digits.")
                continue

            # Convert guess to list of integers
            user_guess = [int(digit) for digit in user_guess]

            # Get feedback for the guess
            black_pegs, white_pegs = self.get_feedback(user_guess)
            self.guesses += 1

            # Print feedback
            print(f"Black pegs: {black_pegs}, White pegs: {white_pegs}")

            # Check if user won
            if black_pegs == 4:
                print(f"Congratulations! You cracked the code in {self.guesses} guesses.")
                break

class AI:
    def __init__(self):
        self.possible_codes = self.generate_possible_codes()

    def generate_possible_codes(self):
        # Generate all possible 4-digit codes
        possible_codes = []
        for i in range(10000):
            code = [int(digit) for digit in f"{i:04d}"]
            possible_codes.append(code)
        return possible_codes

    def make_guess(self):
        # Make a random guess from the possible codes
        return random.choice(self.possible_codes)

    def update_possible_codes(self, guess, black_pegs, white_pegs):
        # Update the possible codes based on the feedback
        self.possible_codes = [code for code in self.possible_codes if self.get_feedback(code, guess) == (black_pegs, white_pegs)]

    def get_feedback(self, code, guess):
        # Calculate feedback for the guess
        black_pegs = 0
        white_pegs = 0
        code_copy = code[:]
        guess_copy = guess[:]

        # Calculate black pegs (correct digit in correct position)
        for i in range(4):
            if guess_copy[i] == code_copy[i]:
                black_pegs += 1
                code_copy[i] = None
                guess_copy[i] = None

        # Calculate white pegs (correct digit in incorrect position)
        for i in range(4):
            if guess_copy[i] is not None and guess_copy[i] in code_copy:
                white_pegs += 1
                code_copy[code_copy.index(guess_copy[i])] = None
                guess_copy[i] = None

        return black_pegs, white_pegs

def main():
    game = CodeBreaker()
    ai = AI()

    while True:
        # Make AI's guess
        ai_guess = ai.make_guess()
        print(f"AI's guess: {''.join(map(str, ai_guess))}")

        # Get feedback for the guess
        black_pegs, white_pegs = game.get_feedback(ai_guess)
        print(f"Black pegs: {black_pegs}, White pegs: {white_pegs}")

        # Update AI's possible codes
        ai.update_possible_codes(ai_guess, black_pegs, white_pegs)

        # Check if AI won
        if black_pegs == 4:
            print(f"AI cracked the code!")
            break

if __name__ == "__main__":
    main()
