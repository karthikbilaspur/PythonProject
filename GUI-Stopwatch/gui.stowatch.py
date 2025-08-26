import tkinter as tk
from threading import Thread
import time

class StopWatch(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.running = False
        self.seconds = 0
        self.display_seconds = "00:00:00"
        self.create_widgets()
        self.update_timer()

    def create_widgets(self):
        self.time_label = tk.Label(self, text=self.display_seconds, font=("Helvetica", 24))
        self.time_label.pack()

        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.pack(side="left")

        self.stop_button = tk.Button(self, text="Stop", command=self.stop, state="disabled")
        self.stop_button.pack(side="left")

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.pack(side="left")

    def update_timer(self):
        if self.running:
            hours, remainder = divmod(self.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.display_seconds = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
            self.time_label.config(text=self.display_seconds)
            self.seconds += 1
        self.master.after(1000, self.update_timer)

    def start(self):
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def reset(self):
        self.running = False
        self.seconds = 0
        self.display_seconds = "00:00:00"
        self.time_label.config(text=self.display_seconds)
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

root = tk.Tk()
app = StopWatch(master=root)
app.mainloop()