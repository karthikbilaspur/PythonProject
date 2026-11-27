import tkinter as tk
from tkinter import messagebox
from typing import Any
from importlib import import_module
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
add_watermark = import_module("add_watermark")
video_to_pdf = import_module("video_to_pdf")
class App:
    def __init__(self):
        self.window = tk.Tk(); self.window.title("Video Editor Suite"); self.window.geometry("480x320")
        tk.Label(self.window, text="✂️ Video Editor Suite", font=("Arial", 16, "bold")).pack(pady=15)
        tk.Label(self.window, text="Choose a tool to open").pack(pady=5)
        tk.Button(self.window, text="1. Add Watermark to Video", width=35, height=2, bg="#9C27B0", fg="white", command=lambda: self.open(add_watermark)).pack(pady=8)
        tk.Button(self.window, text="2. Video to PDF (Frames)", width=35, height=2, bg="#FF9800", fg="white", command=lambda: self.open(video_to_pdf)).pack(pady=8)
        tk.Label(self.window, text="Run: python app.py\nAlso works alone: python add_watermark.py", font=("Arial", 9), fg="gray").pack(pady=15)
        tk.Button(self.window, text="Exit", width=15, command=self.window.destroy).pack()
    def open(self, mod: Any) -> None:
        try: mod.open_window(self.window)
        except Exception as e: messagebox.showerror("Error", str(e))
    def run(self): self.window.mainloop()
if __name__ == "__main__": App().run()
