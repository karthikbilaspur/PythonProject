import tkinter as tk
from random import choice

class Mastermind:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Mastermind Game")
        self.colors = ["red", "green", "blue", "yellow", "orange", "purple"]
        self.code = [choice(self.colors) for _ in range(4)]
        self.guesses = 0
        self.max_guesses = 10
        self.create_widgets()

    def create_widgets(self):
        self.guess_label = tk.Label(self.window, text="Guess the 4 colors (red, green, blue, yellow, orange, purple):")
        self.guess_label.pack()

        self.guess_entry = tk.Entry(self.window)
        self.guess_entry.pack()

        self.guess_button = tk.Button(self.window, text="Guess", command=self.check_guess)
        self.guess_button.pack()

        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack()

        self.guesses_label = tk.Label(self.window, text="Guesses: 0/10")
        self.guesses_label.pack()

        self.history_label = tk.Label(self.window, text="Guess History:")
        self.history_label.pack()

        self.history_text = tk.Text(self.window, height=10, width=40)
        self.history_text.pack()
        self.history_text.config(state="disabled")

    def check_guess(self):
        guess = self.guess_entry.get().split()
        if len(guess) != 4:
            self.result_label['text'] = "Invalid guess. Please enter 4 colors separated by spaces."
            return
        for color in guess:
            if color not in self.colors:
                self.result_label['text'] = "Invalid color. Please enter one of the following colors: red, green, blue, yellow, orange, purple."
                return
        self.guesses += 1
        self.guesses_label['text'] = f"Guesses: {self.guesses}/10"
        black_pegs = 0
        white_pegs = 0
        code_copy = self.code[:]
        guess_copy = guess[:]
        for i in range(4):
            if guess_copy[i] == code_copy[i]:
                black_pegs += 1
                code_copy[i] = None
                guess_copy[i] = None
        for i in range(4):
            if guess_copy[i] is not None and guess_copy[i] in code_copy:
                white_pegs += 1
                code_copy[code_copy.index(guess_copy[i])] = None
                guess_copy[i] = None
        self.result_label['text'] = f"Black pegs: {black_pegs}, White pegs: {white_pegs}"
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, f"Guess {self.guesses}: {' '.join(guess)} - Black pegs: {black_pegs}, White pegs: {white_pegs}\n")
        self.history_text.config(state="disabled")
        if black_pegs == 4:
            self.result_label['text'] = "Congratulations! You won!"
            self.guess_button['state'] = 'disabled'
        elif self.guesses == self.max_guesses:
            self.result_label['text'] = f"Game over! The code was {' '.join(self.code)}"
            self.guess_button['state'] = 'disabled'

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Mastermind()
    game.run()