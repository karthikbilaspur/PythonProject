import tkinter as tk
from random import randint

class DiceRollSimulator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Dice Roll Simulator")

        self.result_label = tk.Label(self.window, text="Result: ", font=("Arial", 24))
        self.result_label.pack()

        self.dice_type_label = tk.Label(self.window, text="Dice Type: ")
        self.dice_type_label.pack()

        self.dice_type_var = tk.StringVar(self.window)
        self.dice_type_var.set("Standard 6-sided")

        self.dice_type_option = tk.OptionMenu(self.window, self.dice_type_var, "Standard 6-sided", "Custom")
        self.dice_type_option.pack()

        self.custom_sides_label = tk.Label(self.window, text="Custom Sides: ")
        self.custom_sides_label.pack()

        self.custom_sides_entry = tk.Entry(self.window)
        self.custom_sides_entry.pack()

        self.num_dice_label = tk.Label(self.window, text="Number of Dice: ")
        self.num_dice_label.pack()

        self.num_dice_entry = tk.Entry(self.window)
        self.num_dice_entry.pack()

        self.roll_button = tk.Button(self.window, text="Roll", command=self.roll_dice)
        self.roll_button.pack()

    def roll_dice(self):
        try:
            if self.dice_type_var.get() == "Standard 6-sided":
                sides = 6
            else:
                sides = int(self.custom_sides_entry.get())

            num_dice = int(self.num_dice_entry.get())

            results = [randint(1, sides) for _ in range(num_dice)]

            if num_dice == 1:
                result_text = f"You rolled a {results[0]}"
            else:
                result_text = f"You rolled: {results}\nTotal: {sum(results)}"

            self.result_label['text'] = f"Result: {result_text}"
        except ValueError:
            self.result_label['text'] = "Invalid input. Please try again."

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    simulator = DiceRollSimulator()
    simulator.run()