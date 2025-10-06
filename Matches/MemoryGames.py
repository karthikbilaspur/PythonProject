import tkinter as tk
import random

class MemoryGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Memory Game")
        self.cards = self.generate_cards()
        self.buttons = []
        self.flipped = []
        self.matches = 0
        self.attempts = 0
        self.create_widgets()
        self.update_score_label()
        self.update_attempts_label()

    def generate_cards(self):
        cards = list(range(8)) * 2
        random.shuffle(cards)
        return cards

    def create_widgets(self):
        self.score_label = tk.Label(self.window, text="Matches: 0")
        self.score_label.grid(row=0, column=0, columnspan=4)
        self.attempts_label = tk.Label(self.window, text="Attempts: 0")
        self.attempts_label.grid(row=1, column=0, columnspan=4)
        for i in range(16):
            button = tk.Button(self.window, text="", width=5, height=3, command=lambda i=i: self.flip(i))
            button.grid(row=i // 4 + 2, column=i % 4)
            self.buttons.append(button)

    def flip(self, i):
        if len(self.flipped) < 2 and self.buttons[i]['text'] == "":
            self.buttons[i]['text'] = str(self.cards[i])
            self.flipped.append(i)
            if len(self.flipped) == 2:
                self.attempts += 1
                self.update_attempts_label()
                self.window.after(500, self.check_match)

    def check_match(self):
        if self.cards[self.flipped[0]] == self.cards[self.flipped[1]]:
            self.matches += 1
            self.update_score_label()
            if self.matches == 8:
                self.window.title("Congratulations! You won!")
                for button in self.buttons:
                    button['state'] = 'disabled'
        else:
            self.buttons[self.flipped[0]]['text'] = ""
            self.buttons[self.flipped[1]]['text'] = ""
        self.flipped = []

    def update_score_label(self):
        self.score_label['text'] = f"Matches: {self.matches}"

    def update_attempts_label(self):
        self.attempts_label['text'] = f"Attempts: {self.attempts}"

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = MemoryGame()
    game.run()