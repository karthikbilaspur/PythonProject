import logic
import tkinter as tk
from tkinter import messagebox
from typing import Optional

class Game2048:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2048 Game")
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.mat: list[list[int]] = logic.start_game()
        self.score: int = 0
        self.undo_stack: list[list[list[int]]] = []
        self.ai_mode = None
        self.create_widgets()
        self.update_grid()

    def create_widgets(self):
        self.grid_labels: list[list[tk.Label]] = []
        for i in range(logic.GRID_SIZE):
            row: list[tk.Label] = []
            for j in range(logic.GRID_SIZE):
                label = tk.Label(self.frame, text="", width=5, height=2, font=("Arial", 24), relief="groove")
                label.grid(row=i, column=j)
                row.append(label)
            self.grid_labels.append(row)
        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.pack()
        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo)
        self.undo_button.pack()
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart)
        self.restart_button.pack()
        self.ai_button_frame = tk.Frame(self.root)
        self.ai_button_frame.pack()
        self.random_ai_button = tk.Button(self.ai_button_frame, text="Random AI", command=self.random_ai)
        self.random_ai_button.pack(side=tk.LEFT)
        self.minimax_ai_button = tk.Button(self.ai_button_frame, text="Minimax AI", command=self.minimax_ai)
        self.minimax_ai_button.pack(side=tk.LEFT)
        self.root.bind("w", self.move_up)
        self.root.bind("a", self.move_left)
        self.root.bind("s", self.move_down)
        self.root.bind("d", self.move_right)

    def update_grid(self):
        for i in range(logic.GRID_SIZE):
            for j in range(logic.GRID_SIZE):
                if self.mat[i][j] == 0:
                    self.grid_labels[i][j].config(text="")
                else:
                    self.grid_labels[i][j].config(text=str(self.mat[i][j]))
        self.score_label.config(text=f"Score: {self.score}")
    def move_up(self, event: Optional[tk.Event] = None):
        if self.ai_mode is None:
            self.undo_stack.append([row[:] for row in self.mat])
            self.mat, changed = logic.move_up(self.mat)
            if changed:
                logic.add_new_2(self.mat)
                self.score += logic.get_score(self.mat)
            self.update_grid()
            self.check_game_over()
    def move_down(self, event: Optional[tk.Event] = None):
        if self.ai_mode is None:
            self.undo_stack.append([row[:] for row in self.mat])
            self.mat, changed = logic.move_down(self.mat)
            if changed:
                logic.add_new_2(self.mat)
                self.score += logic.get_score(self.mat)
            self.update_grid()
            self.check_game_over()
    def move_left(self, event: Optional[tk.Event] = None):
        if self.ai_mode is None:
            self.undo_stack.append([row[:] for row in self.mat])
            self.mat, changed = logic.move_left(self.mat)
            if changed:
                logic.add_new_2(self.mat)
                self.score += logic.get_score(self.mat)
            self.update_grid()
            self.check_game_over()
    def move_right(self, event: Optional[tk.Event] = None):
        if self.ai_mode is None:
            self.undo_stack.append([row[:] for row in self.mat])
            self.mat, changed = logic.move_right(self.mat)
            if changed:
                logic.add_new_2(self.mat)
                self.score += logic.get_score(self.mat)
            self.update_grid()
            self.check_game_over()

    def random_ai(self):
        self.ai_mode = "random"
        self.ai_move()

    def minimax_ai(self):
        self.ai_mode = "minimax"
        self.ai_move()

    def ai_move(self):
        if self.ai_mode == "random":
            self.mat = logic.random_ai_move(self.mat)
        elif self.ai_mode == "minimax":
            self.mat = logic.minimax_ai_move(self.mat)
        logic.add_new_2(self.mat)
        self.score += logic.get_score(self.mat)
        self.update_grid()
        self.check_game_over()
        self.root.after(100, self.ai_move)

    def undo(self):
        if self.undo_stack and self.ai_mode is None:
            self.mat = self.undo_stack.pop()
            self.score -= logic.get_score(self.mat)
            self.update_grid()

    def restart(self):
        self.mat = logic.start_game()
        self.score = 0
        self.undo_stack = []
        self.ai_mode = None
        self.update_grid()

    def check_game_over(self):
        status: str = logic.get_current_state(self.mat)
        if status != "GAME NOT OVER":
            messagebox.showinfo("Game Over", status)  # type: ignore
            self.restart()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = Game2048()
    game.run()