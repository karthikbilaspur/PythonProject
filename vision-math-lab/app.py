import tkinter as tk
from tkinter import messagebox
from importlib import import_module
from typing import Protocol, cast


class WindowModule(Protocol):
 def open_window(self, parent: tk.Misc) -> None: ...


color_tracker = cast(WindowModule, import_module("color-tracker"))
vector_math = cast(WindowModule, import_module("vector-math"))


class App:
 def __init__(self):
  self.window=tk.Tk(); self.window.title("Vision + Math Lab"); self.window.geometry("480x320")
  tk.Label(self.window,text="Vision + Math Lab",font=("Arial",16,"bold")).pack(pady=15)
  tk.Button(self.window,text="1. Color Tracker / Virtual Painter",width=35,height=2,bg="#FF5722",fg="white",command=lambda: self.open(color_tracker)).pack(pady=8)
  tk.Button(self.window,text="2. 3D Vector Math Lab",width=35,height=2,bg="#009688",fg="white",command=lambda: self.open(vector_math)).pack(pady=8)
  tk.Label(self.window,text="Run: python app.py",font=("Arial",9),fg="gray").pack(pady=12)
  tk.Button(self.window,text="Exit",width=15,command=self.window.destroy).pack()
 def open(self, mod: WindowModule) -> None:
  try: mod.open_window(self.window)
  except Exception as e: messagebox.showerror("Error",str(e))
 def run(self): self.window.mainloop()
if __name__=="__main__": App().run()
