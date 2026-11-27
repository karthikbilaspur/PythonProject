"""
Video Converter Suite - Main Launcher
Run: python app.py
Structure:
  app.py               -> main window, calls all tools
  video-reverser.py    -> Video Reverser
  video-to-audio.py    -> Video to Audio (GUI + CLI function)
  video-to-pdf.py      -> Video to PDF
"""
import tkinter as tk
from tkinter import messagebox
import importlib.util
from pathlib import Path
from typing import Protocol, cast


class ToolModule(Protocol):
    def open_window(self, parent: tk.Misc) -> None: ...


def load_tool(module_name: str, filenames: tuple[str, ...]) -> ToolModule:
    tool_path = next(
        (Path(__file__).with_name(name) for name in filenames
         if Path(__file__).with_name(name).is_file()),
        Path(__file__).with_name(filenames[0]),
    )
    spec = importlib.util.spec_from_file_location(module_name, tool_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {module_name} from {tool_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(ToolModule, module)

# Import the 3 tools
video_reverser = load_tool("video_reverser", ("video-reverser.py", "video_reverser.py"))
video_to_audio = load_tool("video_to_audio", ("video-to-audio.py", "video_to_audio.py"))
video_to_pdf = load_tool("video_to_pdf", ("video-to-pdf.py", "video_to_pdf.py"))

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Video Converter Suite")
        self.window.geometry("480x380")
        self.window.resizable(False, False)

        tk.Label(self.window, text="🎬 Video Converter Suite", font=("Arial", 16, "bold")).pack(pady=15)
        tk.Label(self.window, text="Choose a tool to open", font=("Arial", 11)).pack(pady=5)

        tk.Button(self.window, text="1. Video Reverser", width=35, height=2, bg="#2196F3", fg="white",
                  command=self.open_reverser).pack(pady=8)
        tk.Button(self.window, text="2. Video to Audio Converter", width=35, height=2, bg="#4CAF50", fg="white",
                  command=self.open_audio).pack(pady=8)
        tk.Button(self.window, text="3. Video to PDF Converter", width=35, height=2, bg="#FF9800", fg="white",
                  command=self.open_pdf).pack(pady=8)

        tk.Label(self.window, text="Tip: Each tool also works alone\npython video_reverser.py  |  python video_to_audio.py  |  python video_to_pdf.py",
                 font=("Arial", 9), fg="gray", justify="center").pack(pady=15)
        tk.Button(self.window, text="Exit", width=15, command=self.window.destroy).pack()

    def open_reverser(self):
        try:
            video_reverser.open_window(self.window)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_audio(self):
        try:
            video_to_audio.open_window(self.window)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_pdf(self):
        try:
            video_to_pdf.open_window(self.window)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    App().run()
