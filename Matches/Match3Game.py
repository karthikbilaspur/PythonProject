import tkinter as tk
import random

class Match3Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Match-3 Game")
        self.colors = ["red", "green", "blue", "yellow", "orange", "purple"]
        self.grid_size = 8
        self.grid = self.generate_grid()
        self.buttons = []
        self.selected = None
        self.score = 0
        self.moves_left = 100
        self.create_widgets()
        self.update_score_label()
        self.update_moves_label()

    def generate_grid(self):
        grid = []
        for _ in range(self.grid_size):
            row = []
            for _ in range(self.grid_size):
                row.append(random.choice(self.colors))
            grid.append(row)
        return grid

    def create_widgets(self):
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                button = tk.Button(self.window, width=5, height=2, bg=self.grid[i][j], command=lambda i=i, j=j: self.click(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        self.score_label = tk.Label(self.window, text="Score: 0")
        self.score_label.grid(row=self.grid_size, column=0, columnspan=2)
        self.moves_label = tk.Label(self.window, text="Moves Left: 100")
        self.moves_label.grid(row=self.grid_size, column=2, columnspan=2)

    def click(self, i, j):
        if self.selected is None:
            self.selected = (i, j)
            self.buttons[i][j].config(relief="sunken")
        else:
            x, y = self.selected
            self.buttons[x][y].config(relief="raised")
            if abs(x - i) + abs(y - j) == 1:
                self.moves_left -= 1
                self.update_moves_label()
                self.swap(x, y, i, j)
                if not self.check_matches():
                    self.swap(i, j, x, y)
                else:
                    self.score += 10
                    self.update_score_label()
            self.selected = None
            if self.moves_left <= 0:
                self.game_over()

    def swap(self, x1, y1, x2, y2):
        self.grid[x1][y1], self.grid[x2][y2] = self.grid[x2][y2], self.grid[x1][y1]
        self.buttons[x1][y1].config(bg=self.grid[x1][y1])
        self.buttons[x2][y2].config(bg=self.grid[x2][y2])

    def check_matches(self):
        matches = []
        for i in range(self.grid_size):
            for j in range(self.grid_size - 2):
                if self.grid[i][j] == self.grid[i][j+1] == self.grid[i][j+2]:
                    matches.append((i, j))
                    matches.append((i, j+1))
                    matches.append((i, j+2))
        for i in range(self.grid_size - 2):
            for j in range(self.grid_size):
                if self.grid[i][j] == self.grid[i+1][j] == self.grid[i+2][j]:
                    matches.append((i, j))
                    matches.append((i+1, j))
                    matches.append((i+2, j))
        if matches:
            for x, y in set(matches):
                self.buttons[x][y].config(bg="gray")
                self.grid[x][y] = None
            self.window.after(500, self.remove_matches)
            return True
        return False

    def remove_matches(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] is None:
                    self.buttons[i][j].config(bg="SystemButtonFace")
                    for k in range(i, 0, -1):
                        self.grid[k][j] = self.grid[k-1][j]
                        self.buttons[k][j].config(bg=self.grid[k][j])
                    self.grid[0][j] = random.choice(self.colors)
                    self.buttons[0][j].config(bg=self.grid[0][j])

    def update_score_label(self):
        self.score_label['text'] = f"Score: {self.score}"

    def update_moves_label(self):
        self.moves_label['text'] = f"Moves Left: {self.moves_left}"

    def game_over(self):
        for row in self.buttons:
            for button in row:
                button['state'] = 'disabled'
        self.score_label['text'] = f"Game Over! Final Score: {self.score}"

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Match3Game()
    game.run()