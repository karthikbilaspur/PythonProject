import tkinter as tk
from random import choice

class Mastermind:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Mastermind Game")
        self.colors = ["red", "green", "blue", "yellow", "orange", "purple"]
        self.max_guesses = 10
        self.reset_game()
        self.create_widgets()

    def reset_game(self):
        self.code = [choice(self.colors) for _ in range(4)]
        self.guesses = 0

    def create_widgets(self):
        self.guess_label = tk.Label(
            self.window,
            text="Guess the 4 colors (red, green, blue, yellow, orange, purple):"
        )
        self.guess_label.pack()

        self.guess_entry = tk.Entry(self.window)
        self.guess_entry.pack()
        self.guess_entry.bind("<Return>", lambda _event: self.check_guess())
        self.guess_entry.focus()

        self.guess_button = tk.Button(self.window, text="Guess", command=self.check_guess)
        self.guess_button.pack()

        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack()

        self.guesses_label = tk.Label(self.window, text=f"Guesses: 0/{self.max_guesses}")
        self.guesses_label.pack()

        self.history_label = tk.Label(self.window, text="Guess History:")
        self.history_label.pack()

        self.history_text = tk.Text(self.window, height=10, width=40, state="disabled")
        self.history_text.pack()

        self.restart_button = tk.Button(self.window, text="Play Again", command=self.restart)
        self.restart_button.pack()

    def check_guess(self):
        guess = self.guess_entry.get().lower().split()

        if len(guess) != 4:
            self.result_label['text'] = "Invalid guess. Please enter 4 colors separated by spaces."
            return

        for color in guess:
            if color not in self.colors:
                self.result_label['text'] = f"Invalid color '{color}'. Use: {', '.join(self.colors)}"
                return

        self.guesses += 1
        self.guesses_label['text'] = f"Guesses: {self.guesses}/{self.max_guesses}"
        self.guess_entry.delete(0, tk.END)

        black_pegs, white_pegs = self.score_guess(guess)

        self.result_label['text'] = f"Black pegs: {black_pegs}, White pegs: {white_pegs}"

        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, f"Guess {self.guesses}: {' '.join(guess)} - Black: {black_pegs}, White: {white_pegs}\n")
        self.history_text.config(state="disabled")

        if black_pegs == 4:
            self.result_label['text'] = "Congratulations! You won!"
            self.guess_button['state'] = 'disabled'
        elif self.guesses == self.max_guesses:
            self.result_label['text'] = f"Game over! The code was {' '.join(self.code)}"
            self.guess_button['state'] = 'disabled'

    def score_guess(self, guess: list[str]) -> tuple[int, int]:
        black_pegs = 0
        white_pegs = 0
        code_copy: list[str | None] = [color for color in self.code]
        guess_copy: list[str | None] = [color for color in guess]

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

        return black_pegs, white_pegs

    def restart(self):
        self.reset_game()
        self.guesses_label['text'] = f"Guesses: 0/{self.max_guesses}"
        self.result_label['text'] = ""
        self.guess_entry.delete(0, tk.END)
        self.guess_button['state'] = 'normal'
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        self.history_text.config(state="disabled")
        self.guess_entry.focus()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Mastermind()
    game.run()