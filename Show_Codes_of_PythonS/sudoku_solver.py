import tkinter as tk
from tkinter import messagebox

from pyparsing import col

class Sudoku:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sudoku")
        self.window.geometry("300x350")
        self.entry_list = []
        self.create_widgets()

    def create_widgets(self):
        for i in range(9):
            row = []
            for j in range(9):
                e = tk.Entry(self.window, width=2, font=('Arial', 20), justify='center')
                e.grid(row=i, column=j)
                row.append(e)
            self.entry_list.append(row)

        tk.Button(self.window, text="Check", command=self.check_sudoku).grid(row=9, column=0, columnspan=3)
        tk.Button(self.window, text="Clear", command=self.clear_sudoku).grid(row=9, column=3, columnspan=3)
        tk.Button(self.window, text="Solve", command=self.solve_sudoku).grid(row=9, column=6, columnspan=3)

    def check_sudoku(self):
        # Check rows and columns
        for i in range(9):
            row = [int(self.entry_list[i][j].get()) for j in range(9) if self.entry_list[i][j].get()]
            col = [int(self.entry_list[j][i].get()) for j in range(9) if self.entry_list[j][i].get()]
            if len(set(row)) != len(row) or len(set(col)) != len(col):
                messagebox.showerror("Error", "Invalid Sudoku")
                return

        # Check 3x3 boxes
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box = []
                for x in range(3):
                    for y in range(3):
                        val = self.entry_list[i+x][j+y].get()
                        if val:
                            box.append(int(val))
                if len(set(box)) != len(box):
                    messagebox.showerror("Error", "Invalid Sudoku")
                    return

        messagebox.showinfo("Success", "Valid Sudoku")

    def clear_sudoku(self):
        for row in self.entry_list:
            for entry in row:
                entry.delete(0, tk.END)

    def solve_sudoku(self):
        # Simple backtracking algorithm
        def is_valid(num:str , row:str, col:str) -> bool:
            # Check row and column
            for i in range(9):
                if self.entry_list[row][i].get() == str(num) or self.entry_list[i][col].get() == str(num):
                    return False

            # Check 3x3 box
            box_row, box_col = row // 3 * 3, col // 3 * 3
            for i in range(3):
                for j in range(3):
                    if self.entry_list[box_row+i][box_col+j].get() == str(num):
                        return False
            return True

        def solve():
            for i in range(9):
                for j in range(9):
                    if not self.entry_list[i][j].get():
                        for num in range(1, 10):
                            if is_valid(num, i, j):
                                self.entry_list[i][j].delete(0, tk.END)
                                self.entry_list[i][j].insert(0, str(num))
                                if solve():
                                    return True
                                self.entry_list[i][j].delete(0, tk.END)
                        return False
            return True

        solve()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    sudoku = Sudoku()
    sudoku.run()