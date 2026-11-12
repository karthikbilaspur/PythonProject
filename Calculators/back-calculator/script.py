import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class BaseNCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Back_Calculator")
        self.window.geometry("450x350")
        self.icon = tk.PhotoImage(file="./Back_Calculator/data/a_moon_crater.jpeg")
        self.window.iconphoto(False, self.icon)

        image_path = "./Back_Calculator/data/a_moon_crater.jpeg"
        image = Image.open(image_path)
        image = image.resize((450, 350))
        photo = ImageTk.PhotoImage(image)

        background_label = tk.Label(self.window, image=photo)
        background_label.image = photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        # Number entry
        tk.Label(self.window, text="Enter Number:", bg="#CCCCCC", anchor=tk.E, font=("Calibri", 9)).place(x=30, y=30)
        self.num_val = tk.StringVar()
        self.num_entry = tk.Entry(self.window, textvariable=self.num_val, font=("Calibri", 9))
        self.num_entry.place(x=120, y=32)

        # Base-X entry
        tk.Label(self.window, text="Base-X:", bg="#CCCCCC", anchor=tk.E, font=("Calibri", 9)).place(x=250, y=30)
        self.base_x_val = tk.StringVar()
        self.base_x_entry = tk.Entry(self.window, textvariable=self.base_x_val, font=("Calibri", 9), width=5)
        self.base_x_entry.place(x=305, y=32)

        # Base-Y entry
        tk.Label(self.window, text="Base-Y:", bg="#CCCCCC", anchor=tk.E, font=("Calibri", 9)).place(x=250, y=50)
        self.base_y_val = tk.StringVar()
        self.base_y_entry = tk.Entry(self.window, textvariable=self.base_y_val, font=("Calibri", 9), width=5)
        self.base_y_entry.place(x=305, y=52)

        # Calculate button
        tk.Button(self.window, text="Convert", font=("Calibri", 9), command=self.calculate).place(x=180, y=75, width=80)

        # Swap bases button
        tk.Button(self.window, text="Swap Bases", font=("Calibri", 9), command=self.swap_bases).place(x=270, y=75, width=80)

        # Clear button
        tk.Button(self.window, text="Clear", font=("Calibri", 9), command=self.clear_fields).place(x=90, y=75, width=80)

        # Result entry
        tk.Label(self.window, text="Result:", bg="#CCCCCC", anchor=tk.E, font=("Calibri", 9)).place(x=100, y=130)
        self.result_val = tk.StringVar()
        self.result_entry = tk.Entry(self.window, textvariable=self.result_val, font=("Calibri", 9), width=30)
        self.result_entry.configure(state='readonly')
        self.result_entry.place(x=150, y=130)

        # History text box
        tk.Label(self.window, text="History:", bg="#CCCCCC", anchor=tk.E, font=("Calibri", 9)).place(x=30, y=170)
        self.history_text = tk.Text(self.window, font=("Calibri", 9), width=40, height=5)
        self.history_text.place(x=100, y=170)

        # Status bar
        self.status = tk.Label(self.window, text="Hello!! :D", bg="#CCCCCC", fg="green", font=("Calibri", 9), bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=3)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def calculate(self):
        try:
            num = float(self.num_val.get())
            base_x = int(self.base_x_val.get())
            base_y = int(self.base_y_val.get())

            if base_x == base_y or base_x < 2 or base_y < 2:
                self.status.config(text="Huh?! -_- ", fg="orange")
                return

            if base_x == 10:
                result = self.convert_dec_to_base_y(num, base_y)
            elif base_y == 10:
                result = self.convert_base_x_to_dec(num, base_x)
            else:
                result = self.convert_base_x_to_dec(num, base_x)
                result = self.convert_dec_to_base_y(result, base_y)

            self.status.config(text="Successful Conversion! :0 ", fg="green")
            self.result_val.set(result)
            self.result_entry.config(state='normal')
            self.result_entry.config(state='readonly')
            self.update_history(f"{num} (Base {base_x}) = {result} (Base {base_y})")
        except ValueError:
            self.status.config(text="Wrong Input(s)... :\ ", fg="red")

    def swap_bases(self):
        base_x = self.base_x_val.get()
        base_y = self.base_y_val.get()
        self.base_x_val.set(base_y)
        self.base_y_val.set(base_x)

    def clear_fields(self):
        self.num_val.set("")
        self.base_x_val.set("")
        self.base_y_val.set("")
        self.result_val.set("")
        self.result_entry.config(state='normal')
        self.result_entry.config(state='readonly')

    def update_history(self, calculation):
        self.history_text.insert(tk.END, calculation + "\n")

    def convert_base_x_to_dec(self, num, base_x):
        integer_part = str(int(num))[::-1]
        decimal_part = str(num)[str(num).index(".")+1:]
        result = 0

        for i, digit in enumerate(integer_part[::-1]):
            result += int(digit) * (base_x ** i)

        for i, digit in enumerate(decimal_part):
            result += int(digit) * (base_x ** -(i + 1))

        return result

    def convert_dec_to_base_y(self, num, base_y):
        integer_part = int(num)
        decimal_part = num - integer_part
        result_int = []
        result_dec = []

        while integer_part > 0:
            result_int.append(str(int(integer_part % base_y)))
            integer_part //= base_y

        result_int = result_int[::-1]

        while decimal_part > 0:
            decimal_part *= base_y
            digit = int(decimal_part)
            result_dec.append(str(digit))
            decimal_part -= digit

        if result_dec:
            return ' '.join(result_int + ['.'] + result_dec)
        else:
            return ' '.join(result_int)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = BaseNCalculator()
    calculator.run()