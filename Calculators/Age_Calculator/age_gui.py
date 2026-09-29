import tkinter as tk
from tkinter import messagebox
import datetime
import dateparser

class AgeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Age Calculator")

        # Create input field for birthdate
        self.birthdate_label = tk.Label(root, text="Enter your birthdate (in YYYY-MM-DD format or natural language):")
        self.birthdate_label.pack()
        self.birthdate_entry = tk.Entry(root, width=30)
        self.birthdate_entry.pack()

        # Create button to calculate age
        self.calculate_button = tk.Button(root, text="Calculate Age", command=self.calculate_age)
        self.calculate_button.pack()

        # Create label to display age
        self.age_label = tk.Label(root, text="Your age is:")
        self.age_label.pack()
        self.age_result = tk.StringVar()
        self.age_result_label = tk.Label(root, textvariable=self.age_result)
        self.age_result_label.pack()

        # Create label to display detailed age
        self.detailed_age_label = tk.Label(root, text="Detailed Age:")
        self.detailed_age_label.pack()
        self.detailed_age_result = tk.StringVar()
        self.detailed_age_result_label = tk.Label(root, textvariable=self.detailed_age_result)
        self.detailed_age_result_label.pack()

        # Create button to clear fields
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_fields)
        self.clear_button.pack()

    def calculate_age(self):
        birthdate_text = self.birthdate_entry.get()
        try:
            birthdate = dateparser.parse(birthdate_text)
            if birthdate is None:
                messagebox.showerror("Error", "Invalid birthdate. Please try again.")
                return
            today = datetime.date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            self.age_result.set(str(age) + " years old")

            # Calculate detailed age
            months = (today.year - birthdate.year) * 12 + today.month - birthdate.month
            if today.day < birthdate.day:
                months -= 1
            weeks = (today - birthdate).days // 7
            days = (today - birthdate).days
            hours = days * 24
            minutes = hours * 60
            seconds = minutes * 60

            detailed_age = f"Months: {months}\nWeeks: {weeks}\nDays: {days}\nHours: {hours}\nMinutes: {minutes}\nSeconds: {seconds}"
            self.detailed_age_result.set(detailed_age)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields(self):
        self.birthdate_entry.delete(0, tk.END)
        self.age_result.set("")
        self.detailed_age_result.set("")

def main():
    root = tk.Tk()
    app = AgeCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()