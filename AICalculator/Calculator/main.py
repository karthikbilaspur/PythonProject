import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

class Calculator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.frame1 = tk.Frame(self.notebook)
        self.frame2 = tk.Frame(self.notebook)
        self.frame3 = tk.Frame(self.notebook)

        self.notebook.add(self.frame1, text="Basic Calculator")
        self.notebook.add(self.frame2, text="Scientific Calculator")
        self.notebook.add(self.frame3, text="Unit Converter")

        self.basic_calculator()
        self.scientific_calculator()
        self.unit_converter()

    def basic_calculator(self):
        self.entry = tk.Entry(self.frame1, width=35, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            tk.Button(self.frame1, text=button, width=5, command=lambda button=button: self.click_button(button)).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        tk.Button(self.frame1, text="C", width=11, command=self.clear_entry).grid(row=row_val, column=0, columnspan=2)
        tk.Button(self.frame1, text="Del", width=11, command=self.delete_char).grid(row=row_val, column=2, columnspan=2)

    def scientific_calculator(self):
        self.scientific_entry = tk.Entry(self.frame2, width=35, borderwidth=5)
        self.scientific_entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            'sin', 'cos', 'tan', 'log',
            'sqrt', 'x^2', '1/x', 'e^x',
            '(', ')', '=', 'C'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            tk.Button(self.frame2, text=button, width=5, command=lambda button=button: self.scientific_click(button)).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def unit_converter(self):
        tk.Label(self.frame3, text="Length Converter").grid(row=0, column=0, columnspan=2)

        self.length_var = tk.StringVar()
        self.length_var.set("Meter")

        options = ["Meter", "Centimeter", "Millimeter", "Kilometer"]
        tk.OptionMenu(self.frame3, self.length_var, *options).grid(row=1, column=0)

        self.length_entry = tk.Entry(self.frame3, width=10)
        self.length_entry.grid(row=1, column=1)

        tk.Button(self.frame3, text="Convert", command=self.length_convert).grid(row=2, column=0, columnspan=2)

        tk.Label(self.frame3, text="Result:").grid(row=3, column=0)
        self.length_result = tk.Label(self.frame3, text="")
        self.length_result.grid(row=3, column=1)

    def click_button(self, button: str) -> None:
        if button == '=':
            try:
                result = str(eval(self.entry.get()))
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, result)
            except Exception as e:
                messagebox.showerror("Error", str(e))  # type: ignore
        else:
            self.entry.insert(tk.END, button)

    def clear_entry(self):
        self.entry.delete(0, tk.END)

    def delete_char(self):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current[:-1])

    def scientific_click(self, button: str) -> None:
        if button == '=':
            try:
                result = str(eval(self.scientific_entry.get()))
                self.scientific_entry.delete(0, tk.END)
                self.scientific_entry.insert(tk.END, result)
            except Exception as e:
                messagebox.showerror("Error", str(e))  # type: ignore
        elif button == 'C':
            self.scientific_entry.delete(0, tk.END)
        else:
            self.scientific_entry.insert(tk.END, button)

    def length_convert(self):
        try:
            value = float(self.length_entry.get())
            unit = self.length_var.get()
            result = "Invalid unit"

            if unit == "Meter":
                result = f"{value * 100} Centimeter, {value * 1000} Millimeter, {value / 1000} Kilometer"
            elif unit == "Centimeter":
                result = f"{value / 100} Meter, {value * 10} Millimeter, {value / 100000} Kilometer"
            elif unit == "Millimeter":
                result = f"{value / 1000} Meter, {value / 10} Centimeter, {value / 1000000} Kilometer"
            elif unit == "Kilometer":
                result = f"{value * 1000} Meter, {value * 100000} Centimeter, {value * 1000000} Millimeter"

            self.length_result.config(text=result)
        except Exception as e:
            messagebox.showerror("Error", str(e))  # type: ignore

root = tk.Tk()
calc = Calculator(root)
root.mainloop()