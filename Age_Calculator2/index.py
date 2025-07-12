import tkinter as tk
from tkinter import messagebox
from datetime import date

class AgeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Age Calculator")

        # Create input fields
        self.birthdate_label = tk.Label(root, text="Enter your birthdate (YYYY-MM-DD):")
        self.birthdate_label.pack()
        self.birthdate_entry = tk.Entry(root, width=30)
        self.birthdate_entry.pack()

        self.calculate_button = tk.Button(root, text="Calculate Age", command=self.calculate_age)
        self.calculate_button.pack()

        self.age_label = tk.Label(root, text="Your age is:")
        self.age_label.pack()
        self.age_result = tk.StringVar()
        self.age_result_label = tk.Label(root, textvariable=self.age_result)
        self.age_result_label.pack()

        self.detailed_age_label = tk.Label(root, text="Detailed Age:")
        self.detailed_age_label.pack()
        self.detailed_age_result = tk.StringVar()
        self.detailed_age_result_label = tk.Label(root, textvariable=self.detailed_age_result)
        self.detailed_age_result_label.pack()

        self.next_birthday_label = tk.Label(root, text="Days left for next birthday:")
        self.next_birthday_label.pack()
        self.next_birthday_result = tk.StringVar()
        self.next_birthday_result_label = tk.Label(root, textvariable=self.next_birthday_result)
        self.next_birthday_result_label.pack()

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_fields)
        self.clear_button.pack()

        self.age_at_date_label = tk.Label(root, text="Calculate age at specific date (YYYY-MM-DD):")
        self.age_at_date_label.pack()
        self.age_at_date_entry = tk.Entry(root, width=30)
        self.age_at_date_entry.pack()
        self.calculate_age_at_date_button = tk.Button(root, text="Calculate Age at Date", command=self.calculate_age_at_date)
        self.calculate_age_at_date_button.pack()
        self.age_at_date_result = tk.StringVar()
        self.age_at_date_result_label = tk.Label(root, textvariable=self.age_at_date_result)
        self.age_at_date_result_label.pack()

    def calculate_age(self):
        try:
            birthdate_text = self.birthdate_entry.get()
            birthdate = date.fromisoformat(birthdate_text)
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            self.age_result.set(str(age) + " years old")

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

            next_birthday = date(today.year, birthdate.month, birthdate.day)
            if today > next_birthday, next_birthday = date(today.year + 1, birthdate.month, birthdate.day)
            days_left = (next_birthday - today).days
            self.next_birthday_result.set(str(days_left) + " days")

        except ValueError:
            messagebox.showerror("Error", "Invalid birthdate. Please try again.")

    def calculate_age_at_date(self):
        try:
            birthdate_text = self.birthdate_entry.get()
            birthdate = date.fromisoformat(birthdate_text)
            age_at_date_text = self.age_at_date_entry.get()
            age_at_date = date.fromisoformat(age_at_date_text)
            age = age_at_date.year - birthdate.year - ((age_at_date.month, age_at_date.day) < (birthdate.month, birthdate.day))
            self.age_at_date_result.set(str(age) + " years old")

        except ValueError:
            messagebox.showerror("Error", "Invalid birthdate or date. Please try again.")

    def clear_fields(self):
        self.birthdate_entry.delete(0, tk.END)
        self.age_result.set("")
        self.detailed_age_result.set("")
        self.next_birthday_result.set("")
        self.age_at_date_entry.delete(0, tk.END)
        self.age_at_date_result.set("")

def main():
    root = tk.Tk()
    app = AgeCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()