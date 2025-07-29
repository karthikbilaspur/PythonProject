import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.entry = tk.Entry(self.window, width=35, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4)
        self.memory = 0

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            if button == '=':
                tk.Button(self.window, text=button, width=10, command=self.calculate).grid(row=row_val, column=col_val, columnspan=4)
                row_val += 1
            else:
                tk.Button(self.window, text=button, width=10, command=lambda button=button: self.append_to_entry(button)).grid(row=row_val, column=col_val)
                col_val += 1
                if col_val > 3:
                    col_val = 0
                    row_val += 1

        tk.Button(self.window, text="C", width=10, command=self.clear_entry).grid(row=row_val, column=0)
        tk.Button(self.window, text="DEL", width=10, command=self.delete_char).grid(row=row_val, column=1)
        tk.Button(self.window, text="M+", width=10, command=self.memory_add).grid(row=row_val, column=2)
        tk.Button(self.window, text="M-", width=10, command=self.memory_subtract).grid(row=row_val, column=3)
        row_val += 1

        tk.Button(self.window, text="MR", width=10, command=self.memory_recall).grid(row=row_val, column=0)
        tk.Button(self.window, text="MC", width=10, command=self.memory_clear).grid(row=row_val, column=1)
        tk.Button(self.window, text="√", width=10, command=self.sqrt).grid(row=row_val, column=2)
        tk.Button(self.window, text="x^2", width=10, command=self.square).grid(row=row_val, column=3)

    def append_to_entry(self, value):
        self.entry.insert(tk.END, value)

    def calculate(self):
        try:
            result = eval(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_entry(self):
        self.entry.delete(0, tk.END)

    def delete_char(self):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current[:-1])

    def memory_add(self):
        try:
            self.memory += float(self.entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def memory_subtract(self):
        try:
            self.memory -= float(self.entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def memory_recall(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, str(self.memory))

    def memory_clear(self):
        self.memory = 0

    def sqrt(self):
        try:
            result = math.sqrt(float(self.entry.get()))
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def square(self):
        try:
            result = float(self.entry.get()) ** 2
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()