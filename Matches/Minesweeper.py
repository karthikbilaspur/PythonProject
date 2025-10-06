import tkinter as tk
import random

class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        self.width = width
        self.height = height
        self.mines = mines
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flagged = [[False for _ in range(width)] for _ in range(height)]
        self.first_click = True
        self.mines_left = mines

        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.buttons = []
        for i in range(height):
            row = []
            for j in range(width):
                button = tk.Button(self.root, width=2, command=lambda i=i, j=j: self.click(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

        self.flag_button = tk.Button(self.root, text="Flag", command=self.toggle_flag)
        self.flag_button.grid(row=height, column=0, columnspan=width//2)
        self.flagging = False

        self.mines_label = tk.Label(self.root, text=f"Mines left: {mines}")
        self.mines_label.grid(row=height+1, column=0, columnspan=width)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.grid(row=height+2, column=0, columnspan=width)

    def reset(self):
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.revealed = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.flagged = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.first_click = True
        self.mines_left = self.mines
        self.mines_label['text'] = f"Mines left: {self.mines}"
        for row in self.buttons:
            for button in row:
                button.config(text="", state="normal", bg="SystemButtonFace")

    def toggle_flag(self):
        self.flagging = not self.flagging
        if self.flagging:
            self.flag_button['text'] = "Click"
        else:
            self.flag_button['text'] = "Flag"

    def randomize_mines(self, first_i, first_j):
        mines_left = self.mines
        while mines_left > 0:
            i, j = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
            if (i, j) == (first_i, first_j) or self.field[i][j] == -1:
                continue
            self.field[i][j] = -1
            mines_left -= 1

        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j] == -1:
                    continue
                count = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0:
                            continue
                        if i + x < 0 or i + x >= self.height or j + y < 0 or j + y >= self.width:
                            continue
                        if self.field[i + x][j + y] == -1:
                            count += 1
                self.field[i][j] = count

    def reveal(self, i, j):
        if self.revealed[i][j] or self.field[i][j] == -1:
            return
        self.revealed[i][j] = True
        self.buttons[i][j].config(text=str(self.field[i][j]), state="disabled")
        if self.field[i][j] == 0:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue
                    if i + x < 0 or i + x >= self.height or j + y < 0 or j + y >= self.width:
                        continue
                    self.reveal(i + x, j + y)

    def check_win(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j] != -1 and not self.revealed[i][j]:
                    return False
        return True

    def click(self, i, j):
        if self.flagging:
            if self.flagged[i][j]:
                self.buttons[i][j].config(text="", bg="SystemButtonFace")
                self.flagged[i][j] = False
                self.mines_left += 1
            else:
                self.buttons[i][j].config(text="F", bg="blue")
                self.flagged[i][j] = True
                self.mines_left -= 1
            self.mines_label['text'] = f"Mines left: {self.mines_left}"
            return

        if self.first_click:
            self.randomize_mines(i, j)
            self.first_click = False
        if self.field[i][j] == -1:
            self.buttons[i][j].config(text="X", bg="red")
            for x in range(self.height):
                for y in range(self.width):
                    if self.field[x][y] == -1:
                        self.buttons[x][y].config(text="X", bg="red")
                    else:
                        self.buttons[x][y].config(state="disabled")
            self.reset_button.config(text="Game Over! Reset?")
        else:
            self.reveal(i, j)
            if self.check_win():
                self.reset_button.config(text="You Won! Reset?")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = Minesweeper()
    game.run()