import tkinter as tk
from threading import Thread
import time

class Stopwatch:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stopwatch")
        self.label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 80))
        self.label.pack()
        self.running = False
        self.seconds = 0
        self.display_time()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_stopwatch)
        self.start_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_stopwatch, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_stopwatch)
        self.reset_button.pack(side=tk.LEFT)

    def display_time(self):
        if self.running:
            self.seconds += 1
            hours, remainder = divmod(self.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.label.config(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")
        self.root.after(1000, self.display_time)

    def start_stopwatch(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_stopwatch(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def reset_stopwatch(self):
        self.running = False
        self.seconds = 0
        self.label.config(text="00:00:00")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    stopwatch = Stopwatch()
    stopwatch.run()