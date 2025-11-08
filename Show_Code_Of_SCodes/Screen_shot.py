import cv2
import numpy as np
from PIL import ImageGrab
import time
import pyautogui
import tkinter as tk
from tkinter import ttk

class ScreenCaptureTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Capture Tool")
        self.root.geometry("400x300")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.screen_recorder_frame = tk.Frame(self.notebook)
        self.screenshot_frame = tk.Frame(self.notebook)
        self.delayed_screenshot_frame = tk.Frame(self.notebook)

        self.notebook.add(self.screen_recorder_frame, text="Screen Recorder")
        self.notebook.add(self.screenshot_frame, text="Screenshot")
        self.notebook.add(self.delayed_screenshot_frame, text="Delayed Screenshot")

        self.screen_recorder_ui()
        self.screenshot_ui()
        self.delayed_screenshot_ui()

    def screen_recorder_ui(self):
        label = tk.Label(self.screen_recorder_frame, text="Screen Recorder")
        label.pack(pady=10)

        button = tk.Button(self.screen_recorder_frame, text="Start Recording", command=self.screenrecorder)
        button.pack(pady=20)

    def screenshot_ui(self):
        label = tk.Label(self.screenshot_frame, text="Take a Screenshot")
        label.pack(pady=10)

        button = tk.Button(self.screenshot_frame, text="Take Screenshot", command=self.screenshot)
        button.pack(pady=20)

    def delayed_screenshot_ui(self):
        label = ttk.Label(self.delayed_screenshot_frame, text="Delay (in seconds):")
        label.pack(pady=10)
        self.delay_entry = ttk.Entry(self.delayed_screenshot_frame)
        self.delay_entry.pack(pady=5)
        self.delay_entry.insert(0, "5.0")

        button = ttk.Button(self.delayed_screenshot_frame, text="Take Screenshot", command=self.on_take_screenshot)
        button.pack(pady=20)

    def screenrecorder(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        name = int(round(time.time() * 1000))
        name = '{}.avi'.format(name)
        out = cv2.VideoWriter(name, fourcc, 5.0, (1920, 1080))

        while True:
            img = ImageGrab.grab()
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            cv2.imshow("Screen Recorder", frame)
            out.write(frame)

            if cv2.waitKey(1) == 27:
                break

        out.release()
        cv2.destroyAllWindows()

    def screenshot(self):
        name = int(round(time.time() * 1000))
        name = '{}.png'.format(name)
        img = pyautogui.screenshot(name)
        img.show()

    def on_take_screenshot(self):
        delay = float(self.delay_entry.get())
        self.take_screenshot(delay)

    def take_screenshot(self, delay):
        name = int(round(time.time() * 1000))
        name = '{}.png'.format(name)
        time.sleep(delay)
        img = pyautogui.screenshot(name)
        img.show()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ScreenCaptureTool()
    app.run()