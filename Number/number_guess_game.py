import tkinter as tk
from random import randint

class NumberGuessingGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Number Guessing Game")
        self.window.geometry("300x150")

        self.number_to_guess = randint(1, 100)
        self.guesses = 0

        self.label = tk.Label(self.window, text="Guess a number between 1 and 100")
        self.label.pack()

        self.entry = tk.Entry(self.window)
        self.entry.pack()

        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack()

        self.guess_button = tk.Button(self.window, text="Guess", command=self.guess_number)
        self.guess_button.pack()

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_game)
        self.reset_button.pack()

    def guess_number(self):
        try:
            guess = int(self.entry.get())
            self.guesses += 1

            if guess < self.number_to_guess:
                self.result_label['text'] = "Too low! Try again."
            elif guess > self.number_to_guess:
                self.result_label['text'] = "Too high! Try again."
            else:
                self.result_label['text'] = f"Congratulations! You found the number in {self.guesses} guesses."
                self.guess_button['state'] = 'disabled'
        except ValueError:
            self.result_label['text'] = "Invalid input. Please enter a number."

    def reset_game(self):
        self.number_to_guess = randint(1, 100)
        self.guesses = 0
        self.result_label['text'] = ""
        self.guess_button['state'] = 'normal'
        self.entry.delete(0, tk.END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = NumberGuessingGame()
    game.run()