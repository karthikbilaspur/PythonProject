import time
import tkinter as tk

class DigitalClock:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Digital Clock")

        self.time_label = tk.Label(self.window, font=('Arial', 48), fg='blue')
        self.time_label.pack()

        self.date_label = tk.Label(self.window, font=('Arial', 24), fg='green')
        self.date_label.pack()

        self.alarm_label = tk.Label(self.window, font=('Arial', 24), fg='red')
        self.alarm_label.pack()

        self.alarm_entry = tk.Entry(self.window, font=('Arial', 24))
        self.alarm_entry.pack()

        self.set_alarm_button = tk.Button(self.window, text="Set Alarm", command=self.set_alarm)
        self.set_alarm_button.pack()

        self.alarm_time = None
        self.update_time()
        self.window.mainloop()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        current_date = time.strftime("%Y-%m-%d")
        self.date_label.config(text=current_date)

        if self.alarm_time and current_time == self.alarm_time:
            self.alarm_label.config(text="Wake Up!")
            self.alarm_time = None
        else:
            self.alarm_label.config(text="")

        self.window.after(1000, self.update_time)

    def set_alarm(self):
        self.alarm_time = self.alarm_entry.get()
        self.alarm_label.config(text=f"Alarm set for {self.alarm_time}")

if __name__ == "__main__":
    clock = DigitalClock()