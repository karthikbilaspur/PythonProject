"""
Pomodoro Timer - Medium Level (Tkinter)
Features: work / short break / long break cycle, custom durations,
pause/resume, skip, session stats, progress bar, sound via bell, no crash on bad input.
"""
import tkinter as tk
from tkinter import ttk, messagebox

class PomodoroTimer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("380x420")
        self.root.resizable(False, False)

        self.work_min = tk.IntVar(value=25)
        self.short_min = tk.IntVar(value=5)
        self.long_min = tk.IntVar(value=15)
        self.cycles_before_long = 4

        self.mode = "Work"  # Work / Short Break / Long Break
        self.seconds_left = self.work_min.get() * 60
        self.completed = 0
        self.running = False
        self.after_id = None

        ttk.Label(root, text="POMODORO", font=("Helvetica", 20, "bold")).pack(pady=10)
        self.mode_label = ttk.Label(root, text="Work Session", font=("Helvetica", 13))
        self.mode_label.pack()
        self.time_label = ttk.Label(root, text="25:00", font=("Helvetica", 48, "bold"))
        self.time_label.pack(pady=5)
        self.progress = ttk.Progressbar(root, length=300, mode="determinate")
        self.progress.pack(pady=5)
        self.stats_label = ttk.Label(root, text="Completed Pomodoros: 0")
        self.stats_label.pack()

        btn = ttk.Frame(root); btn.pack(pady=10)
        self.start_btn = ttk.Button(btn, text="Start", command=self.toggle)
        self.start_btn.grid(row=0, column=0, padx=5)
        ttk.Button(btn, text="Skip", command=self.skip).grid(row=0, column=1, padx=5)
        ttk.Button(btn, text="Reset", command=self.reset).grid(row=0, column=2, padx=5)

        settings = ttk.LabelFrame(root, text="Settings (minutes)"); settings.pack(padx=15, pady=10, fill="x")
        for i, (label, var) in enumerate([("Work", self.work_min), ("Short Break", self.short_min), ("Long Break", self.long_min)]):
            ttk.Label(settings, text=label).grid(row=i, column=0, sticky="w", padx=8, pady=3)
            ttk.Spinbox(settings, from_=1, to=120, textvariable=var, width=8, command=self.apply_settings).grid(row=i, column=1, padx=8, pady=3)
        ttk.Label(settings, text="Tip: Press Start to begin. After 4 works you get a long break.").grid(row=3, column=0, columnspan=2, padx=8, pady=5)
        self.apply_settings()

    def total_for_mode(self):
        return {"Work": self.work_min.get(), "Short Break": self.short_min.get(), "Long Break": self.long_min.get()}[self.mode] * 60

    def apply_settings(self):
        if not self.running:
            self.seconds_left = self.total_for_mode()
            self.update_display()

    def update_display(self):
        m, s = divmod(max(0, self.seconds_left), 60)
        self.time_label.config(text=f"{m:02d}:{s:02d}")
        total = self.total_for_mode() or 1
        self.progress["value"] = (total - self.seconds_left) / total * 100
        self.mode_label.config(text=f"{self.mode}  •  Cycle {self.completed + 1 if self.mode=='Work' else self.completed}/{self.cycles_before_long}")

    def toggle(self):
        if self.running: self.pause()
        else:
            self.running = True; self.start_btn.config(text="Pause"); self.tick()

    def pause(self):
        self.running = False; self.start_btn.config(text="Resume")
        if self.after_id: self.root.after_cancel(self.after_id); self.after_id = None

    def tick(self):
        if not self.running: return
        self.seconds_left -= 1
        self.update_display()
        if self.seconds_left <= 0:
            self.root.bell()
            self.next_phase()
            return
        self.after_id = self.root.after(1000, self.tick)

    def next_phase(self):
        self.pause()
        if self.mode == "Work":
            self.completed += 1
            self.stats_label.config(text=f"Completed Pomodoros: {self.completed}")
            if self.completed % self.cycles_before_long == 0:
                self.mode = "Long Break"; msg = "Great work! Time for a long break."
            else:
                self.mode = "Short Break"; msg = "Work done! Time for a short break."
        else:
            self.mode = "Work"; msg = "Break over! Back to work."
        self.seconds_left = self.total_for_mode(); self.update_display()
        messagebox.showinfo("Pomodoro", msg)

    def skip(self):
        self.pause(); self.next_phase()

    def reset(self):
        self.pause(); self.mode = "Work"; self.completed = 0
        self.stats_label.config(text="Completed Pomodoros: 0")
        self.seconds_left = self.total_for_mode(); self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    PomodoroTimer(root)
    root.mainloop()
