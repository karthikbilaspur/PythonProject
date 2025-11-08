import tkinter as tk
from math import sin, cos, tan, log, sqrt, exp, pi, e

class Calculator:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.entry = tk.Entry(master, width=35, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'sin', 'cos', 'tan', 'log',
            'sqrt', 'exp', '(', ')',
            'C', 'e', 'pi', '^'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            tk.Button(self.master, text=button, width=10, command=lambda button=button: self.on_click(button)).grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def on_click(self, button: str):
        if button == '=':
            try:
                expression = self.entry.get()
                # Create a dictionary with math functions
                from typing import Any, Dict
                math_context: dict[str, Any] = {
                    'sin': sin, 'cos': cos, 'tan': tan,
                    'log': log, 'sqrt': sqrt, 'exp': exp,
                    'pi': pi, 'e': e
                }
                result = eval(expression, {"__builtins__": {}}, math_context)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        elif button == 'C':
            self.entry.delete(0, tk.END)
        elif button == 'sin':
            self.entry.insert(tk.END, 'sin(')
        elif button == 'cos':
            self.entry.insert(tk.END, 'cos(')
        elif button == 'tan':
            self.entry.insert(tk.END, 'tan(')
        elif button == 'log':
            self.entry.insert(tk.END, 'log(')
        elif button == 'sqrt':
            self.entry.insert(tk.END, 'sqrt(')
        elif button == 'exp':
            self.entry.insert(tk.END, 'exp(')
        elif button == 'pi':
            self.entry.insert(tk.END, str(pi))
        elif button == 'e':
            self.entry.insert(tk.END, str(e))
        elif button == '^':
            self.entry.insert(tk.END, '**')
        else:
            self.entry.insert(tk.END, button)

root = tk.Tk()
root.title("Enhanced Scientific Calculator")
calc = Calculator(root)
root.mainloop()