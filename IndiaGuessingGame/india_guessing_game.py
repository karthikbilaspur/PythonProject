import tkinter as tk
from random import choice

# Parse states from search results
states = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
]

class StateGuessingGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("India State Guessing Game")
        self.state_to_guess = choice(states)
        self.guessed = False
        self.guess_count = 0

        self.state_label = tk.Label(self.root, text="Guess an Indian state:", font=('Arial', 16))
        self.state_label.pack()

        self.entry = tk.Entry(self.root, font=('Arial', 16))
        self.entry.pack()

        self.result_label = tk.Label(self.root, text="", font=('Arial', 16))
        self.result_label.pack()

        self.guess_button = tk.Button(self.root, text="Guess", command=self.check_guess, font=('Arial', 16))
        self.guess_button.pack()

        self.hint_button = tk.Button(self.root, text="Hint", command=self.give_hint, font=('Arial', 16))
        self.hint_button.pack()

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game, font=('Arial', 16))
        self.new_game_button.pack()

    def check_guess(self):
        guess = self.entry.get()
        self.guess_count += 1
        if guess.lower() == self.state_to_guess.lower():
            self.result_label.config(text=f"Correct! The state was {self.state_to_guess}. You guessed it in {self.guess_count} attempts.")
            self.guessed = True
        else:
            self.result_label.config(text="Incorrect. Try again!")

    def give_hint(self):
        if not self.guessed:
            first_letter = self.state_to_guess[0]
            self.result_label.config(text=f"Hint: The state starts with '{first_letter}'.")
        else:
            self.result_label.config(text="You've already guessed the state!")

    def new_game(self):
        self.state_to_guess = choice(states)
        self.guessed = False
        self.guess_count = 0
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = StateGuessingGame()
    game.run()