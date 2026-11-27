import tkinter as tk
from tkinter import messagebox
import importlib
from typing import Protocol, cast

class WindowModule(Protocol):
  def open_window(self, parent: tk.Tk) -> None: ...

class App:
  def __init__(self):
    self.window = tk.Tk()
    self.window.title("Voice AI Suite")
    self.window.geometry("480x380")
    tk.Label(self.window, text="Voice AI Suite", font=("Arial", 16, "bold")).pack(pady=15)
    tk.Button(
      self.window,
      text="1. Voice Assistant (Robot)",
      width=35,
      height=2,
      bg="#673AB7",
      fg="white",
      command=lambda: self.open("voice-assistant"),
    ).pack(pady=8)
    tk.Button(
      self.window,
      text="2. Voice Calculator",
      width=35,
      height=2,
      bg="#2196F3",
      fg="white",
      command=lambda: self.open("voice-calculator"),
    ).pack(pady=8)
    tk.Button(
      self.window,
      text="3. Audio Recorder",
      width=35,
      height=2,
      bg="#F44336",
      fg="white",
      command=lambda: self.open("audio-recorder"),
    ).pack(pady=8)
    tk.Label(self.window, text="Run: python app.py", font=("Arial", 9), fg="gray").pack(pady=12)
    tk.Button(self.window, text="Exit", width=15, command=self.window.destroy).pack()

  def open(self, mod: str | WindowModule) -> None:
    try:
      if isinstance(mod, str):
        mod = cast(WindowModule, importlib.import_module(mod))
      mod.open_window(self.window)
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def run(self) -> None:
    self.window.mainloop()


if __name__ == "__main__":
  App().run()
