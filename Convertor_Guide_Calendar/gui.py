import tkinter as tk
from calendar import  monthcalendar
from datetime import datetime
import calendar

class Calendar:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calendar")
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.cal = monthcalendar(self.year, self.month)

        self.setup_gui()

    def setup_gui(self):
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill="both", expand=True)

        self.label = tk.Label(self.frame, text=calendar.month_name[self.month] + " " + str(self.year), font=("Arial", 24))
        self.label.pack(fill="x")

        self.weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.weekday_row = tk.Frame(self.frame)
        for name in self.weekday_names:
            tk.Label(self.weekday_row, text=name, width=5).pack(side="left")
        self.weekday_row.pack(fill="x")

        self.calendar_frame = tk.Frame(self.frame)
        for week in self.cal:
            row = tk.Frame(self.calendar_frame)
            for day in week:
                if day == 0:
                    label = tk.Label(row, text="", width=5)
                else:
                    label = tk.Label(row, text=str(day), width=5)
                    if day == datetime.now().day and self.month == datetime.now().month and self.year == datetime.now().year:
                        label.config(bg="blue", fg="white")
                label.pack(side="left")
            row.pack(fill="x")
        self.calendar_frame.pack(fill="both", expand=True)

        self.button_frame = tk.Frame(self.frame)
        tk.Button(self.button_frame, text="Previous Month", command=self.prev_month).pack(side="left")
        tk.Button(self.button_frame, text="Next Month", command=self.next_month).pack(side="left")
        tk.Button(self.button_frame, text="Get Month Range", command=self.get_month_range).pack(side="label.config(text=f"Days in month: {monthrange(self.year, self.month)[1]}")
        self.button_frame.pack(fill="x")

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.update_calendar()

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        self.cal = monthcalendar(self.year, self.month)
        for week in self.cal:
            row = tk.Frame(self.calendar_frame)
            for day in week:
                if day == 0:
                    label = tk.Label(row, text="", width=5)
                else:
                    label = tk.Label(row, text=str(day), width=5)
                    if day == datetime.now().day and self.month == datetime.now().month and self.year == datetime.now().year:
                        label.config(bg="blue", fg="white")
                label.pack(side="left")
            row.pack(fill="x")
        self.label.config(text=calendar.month_name[self.month] + " " + str(self.year))

    def get_month_range(self):
        days_in_month = monthrange(self.year, self.month)[1]
        self.label.config(text=f"Days in month: {days_in_month}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calendar = Calendar()
    calendar.run()