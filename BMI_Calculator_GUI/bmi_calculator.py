import tkinter as tk
from tkinter import messagebox

class BMICalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("BMI Calculator")

        # Create input fields
        self.weight_label = tk.Label(self.window, text="Weight (in kg):")
        self.weight_label.grid(row=0, column=0, padx=5, pady=5)
        self.weight_entry = tk.Entry(self.window)
        self.weight_entry.grid(row=0, column=1, padx=5, pady=5)

        self.height_label = tk.Label(self.window, text="Height (in meters):")
        self.height_label.grid(row=1, column=0, padx=5, pady=5)
        self.height_entry = tk.Entry(self.window)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create calculate button
        self.calculate_button = tk.Button(self.window, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Create result label
        self.result_label = tk.Label(self.window, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = weight / (height ** 2)
            category = self.get_category(bmi)
            result = f"Your BMI is: {bmi:.2f}\nYou are {category}"
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height values")

    def get_category(self, bmi):
        if bmi < 18.5:
            return "underweight"
        elif bmi < 25:
            return "normal weight"
        elif bmi < 30:
            return "overweight"
        else:
            return "obese"

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = BMICalculator()
    calculator.run()