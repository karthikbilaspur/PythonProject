"""
Screen Capture Tool — screenshot, delayed screenshot, screen recorder.
Fixes vs original: recorder no longer freezes Tkinter (runs in a thread),
has a real Stop button, uses actual screen size instead of hardcoded
1920x1080, and fixes the colour conversion (PIL gives RGB, OpenCV wants BGR).

Requires: pip install opencv-python numpy pillow pyautogui
Note: ImageGrab.grab() works on Windows/macOS. On Linux use X11 + `scrot`
or replace grab with pyautogui.screenshot().
"""
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab


class ScreenCaptureTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Capture Tool")
        self.root.geometry("400x320")
        self.recording = False
        self.rec_thread = None

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        self.rec_frame = tk.Frame(self.notebook)
        self.shot_frame = tk.Frame(self.notebook)
        self.delay_frame = tk.Frame(self.notebook)
        self.notebook.add(self.rec_frame, text="Screen Recorder")
        self.notebook.add(self.shot_frame, text="Screenshot")
        self.notebook.add(self.delay_frame, text="Delayed Screenshot")

        self._recorder_ui()
        self._screenshot_ui()
        self._delayed_ui()

    # --- UI ---
    def _recorder_ui(self):
        tk.Label(self.rec_frame, text="Screen Recorder").pack(pady=10)
        self.rec_btn = tk.Button(self.rec_frame, text="Start Recording", command=self.toggle_recording)
        self.rec_btn.pack(pady=10)
        tk.Label(self.rec_frame, text="Press Stop (or Esc in preview window)\nto finish. File saved as <timestamp>.avi",
                 fg="grey").pack()

    def _screenshot_ui(self):
        tk.Label(self.shot_frame, text="Take a Screenshot").pack(pady=10)
        tk.Button(self.shot_frame, text="Take Screenshot", command=self.screenshot).pack(pady=20)

    def _delayed_ui(self):
        tk.Label(self.delay_frame, text="Delay (in seconds):").pack(pady=10)
        self.delay_entry = ttk.Entry(self.delay_frame)
        self.delay_entry.pack(pady=5)
        self.delay_entry.insert(0, "5")
        tk.Button(self.delay_frame, text="Take Screenshot", command=self.on_delayed).pack(pady=20)

    # --- Recorder (threaded so UI stays responsive) ---
    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.rec_btn.config(text="Stop Recording")
            self.rec_thread = threading.Thread(target=self._record_loop, daemon=True)
            self.rec_thread.start()
        else:
            self.recording = False
            self.rec_btn.config(text="Start Recording")

    def _record_loop(self):
        w, h = pyautogui.size()  # real screen size, not hardcoded 1920x1080
        name = f"{int(time.time()*1000)}.avi"
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(name, fourcc, 10.0, (w, h))
        try:
            while self.recording:
                img = ImageGrab.grab()
                # PIL -> numpy is RGB; VideoWriter expects BGR
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                out.write(frame)
                cv2.imshow("Screen Recorder — press Esc to stop", frame)
                if cv2.waitKey(1) == 27:
                    break
        finally:
            out.release()
            cv2.destroyAllWindows()
            self.recording = False
            self.root.after(0, lambda: self.rec_btn.config(text="Start Recording"))
            self.root.after(0, lambda: messagebox.showinfo("Saved", f"Recording saved as {name}"))

    # --- Screenshots ---
    def screenshot(self):
        name = f"{int(time.time()*1000)}.png"
        pyautogui.screenshot(name)
        messagebox.showinfo("Saved", f"Screenshot saved as {name}")

    def on_delayed(self):
        try:
            delay = float(self.delay_entry.get())
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Delay must be a non-negative number")
            return
        # Don't block the UI with time.sleep — schedule it
        self.root.after(int(delay * 1000), self.screenshot)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ScreenCaptureTool().run()
