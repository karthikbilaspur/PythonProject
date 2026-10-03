import tkinter as tk
from tkinter import messagebox

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.label = tk.Label(self.root, text="25:00", font=("Helvetica", 48))
        self.label.pack()
        self.seconds = 1500  # 25 minutes
        self.break_time = False
        self.running = False
        self.pomodoros = 0
        self.button = tk.Button(self.root, text="Start", command=self.start_timer)
        self.button.pack()
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_timer)
        self.reset_button.pack()
        self.pomodoro_label = tk.Label(self.root, text="Pomodoros: 0")
        self.pomodoro_label.pack()
        self.work_time_label = tk.Label(self.root, text="Work Time (minutes):")
        self.work_time_label.pack()
        self.work_time_entry = tk.Entry(self.root)
        self.work_time_entry.insert(0, "25")
        self.work_time_entry.pack()
        self.break_time_label = tk.Label(self.root, text="Break Time (minutes):")
        self.break_time_label.pack()
        self.break_time_entry = tk.Entry(self.root)
        self.break_time_entry.insert(0, "5")
        self.break_time_entry.pack()
        self.set_time_button = tk.Button(self.root, text="Set Time", command=self.set_time)
        self.set_time_button.pack()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.button.config(text="Stop", command=self.stop_timer)
            self.update_timer()

    def stop_timer(self):
        if self.running:
            self.running = False
            self.button.config(text="Start", command=self.start_timer)

    def reset_timer(self):
        self.running = False
        self.seconds = int(self.work_time_entry.get()) * 60
        self.break_time = False
        self.pomodoros = 0
        self.pomodoro_label.config(text=f"Pomodoros: {self.pomodoros}")
        self.label.config(text=f"{int(self.work_time_entry.get()):02d}:00")
        self.button.config(text="Start", command=self.start_timer)

    def set_time(self):
        self.work_time = int(self.work_time_entry.get())
        self.break_time_minutes = int(self.break_time_entry.get())
        self.seconds = self.work_time * 60
        self.label.config(text=f"{self.work_time:02d}:00")

    def update_timer(self):
        if self.running:
            minutes, seconds = divmod(self.seconds, 60)
            self.label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.seconds -= 1
            if self.seconds < 0:
                if self.break_time:
                    self.seconds = int(self.work_time_entry.get()) * 60
                    self.break_time = False
                    self.pomodoros += 1
                    self.pomodoro_label.config(text=f"Pomodoros: {self.pomodoros}")
                    messagebox.showinfo("Pomodoro Timer", "Back to work!")
                else:
                    self.seconds = int(self.break_time_entry.get()) * 60
                    self.break_time = True
                    messagebox.showinfo("Pomodoro Timer", "Time for a break!")
            self.root.after(1000, self.update_timer)

    def run(self):
        self.set_time()
        self.root.mainloop()

if __name__ == "__main__":
    timer = PomodoroTimer()
    timer.run()