import tkinter as tk
import random
import time

class MemoryGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Memory Game")
        self.symbols = ["🍎", "🍌", "🍇", "🍓", "🍊", "🥝", "🍒", "🍑"]
        self.colors = ["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF", "#FF9F45", "#B983FF", "#FF6FB5", "#00C9A7"]
        self.cols = 4
        self.rows = 4
        self.buttons: list[tk.Button] = []
        self.flipped: list[int] = []
        self.cards: list[tuple[str, str]] = []
        self.reset_game()
        self.create_widgets()
        self.start_timer()

    def reset_game(self):
        # Pair each symbol with a color, shuffle
        pairs = list(zip(self.symbols, self.colors))
        self.cards = pairs * 2
        random.shuffle(self.cards)
        self.flipped = []
        self.matches = 0
        self.attempts = 0
        self.locked = False
        self.start_time = time.time()
        self.won = False

    def create_widgets(self):
        self.top_frame = tk.Frame(self.window)
        self.top_frame.grid(row=0, column=0, columnspan=self.cols, pady=5)

        self.score_label = tk.Label(self.top_frame, text="Matches: 0/8", font=("Arial", 12, "bold"))
        self.score_label.pack(side="left", padx=10)

        self.attempts_label = tk.Label(self.top_frame, text="Attempts: 0", font=("Arial", 12))
        self.attempts_label.pack(side="left", padx=10)

        self.timer_label = tk.Label(self.top_frame, text="Time: 0s", font=("Arial", 12))
        self.timer_label.pack(side="left", padx=10)

        self.restart_button = tk.Button(self.top_frame, text="Restart", command=self.restart)
        self.restart_button.pack(side="left", padx=10)

        self.status_label = tk.Label(self.window, text="Find all matching pairs!", font=("Arial", 11))
        self.status_label.grid(row=1, column=0, columnspan=self.cols, pady=2)

        self.buttons = []
        for i in range(self.rows * self.cols):
            button = tk.Button(
                self.window, text="?", width=6, height=3,
                font=("Arial", 20), bg="#E0E0E0",
                command=lambda i=i: self.flip(i)
            )
            button.grid(row=i // self.cols + 2, column=i % self.cols, padx=3, pady=3)
            self.buttons.append(button)

    def start_timer(self):
        if not self.won:
            elapsed = int(time.time() - self.start_time)
            self.timer_label['text'] = f"Time: {elapsed}s"
            self.window.after(1000, self.start_timer)

    def flip(self, i: int):
        if self.locked or self.won:
            return
        if i in self.flipped:
            return
        if self.buttons[i]['text'] != "?":
            return  # already matched

        symbol, color = self.cards[i]
        self.buttons[i].config(text=symbol, bg=color)
        self.flipped.append(i)

        if len(self.flipped) == 2:
            self.attempts += 1
            self.attempts_label['text'] = f"Attempts: {self.attempts}"
            self.locked = True
            self.window.after(600, self.check_match)

    def check_match(self):
        a, b = self.flipped
        if self.cards[a] == self.cards[b]:
            # Match - keep them face up, dim them slightly
            self.matches += 1
            self.score_label['text'] = f"Matches: {self.matches}/8"
            self.buttons[a].config(state="disabled", bg="#C8E6C9")
            self.buttons[b].config(state="disabled", bg="#C8E6C9")
            self.status_label['text'] = "Nice match! 🎉"

            if self.matches == 8:
                self.won = True
                elapsed = int(time.time() - self.start_time)
                self.status_label['text'] = f"You won in {self.attempts} attempts and {elapsed}s!"
                self.window.title("Memory Game - You Won!")
        else:
            # Mismatch - flash red, then flip back
            self.buttons[a].config(bg="#FFCDD2")
            self.buttons[b].config(bg="#FFCDD2")
            self.status_label['text'] = "Not a match, try again!"
            self.window.after(200, lambda: self.flip_back(a, b))
            self.flipped = []
            self.locked = False
            return

        self.flipped = []
        self.locked = False

    def flip_back(self, a: int, b: int):
        for idx in (a, b):
            self.buttons[idx].config(text="?", bg="#E0E0E0")

    def restart(self):
        self.reset_game()
        self.won = False
        self.window.title("Memory Game")
        self.score_label['text'] = "Matches: 0/8"
        self.attempts_label['text'] = "Attempts: 0"
        self.status_label['text'] = "Find all matching pairs!"
        for btn in self.buttons:
            btn.config(text="?", bg="#E0E0E0", state="normal")
        self.start_timer()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = MemoryGame()
    game.run()