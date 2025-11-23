import tkinter as tk
from tkinter import filedialog
import cv2
from moviepy.editor import *

class VideoReverser:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Video Reverser")

        # Create GUI elements
        self.file_label = tk.Label(self.window, text="Select a video file:")
        self.file_label.pack()

        self.file_entry = tk.Entry(self.window, width=50)
        self.file_entry.pack()

        self.browse_button = tk.Button(self.window, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.reverse_button = tk.Button(self.window, text="Reverse Video", command=self.reverse_video)
        self.reverse_button.pack()

        self.save_label = tk.Label(self.window, text="")
        self.save_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4 .avi .mov")])
        self.file_entry.insert(0, file_path)

    def reverse_video(self):
        file_path = self.file_entry.get()
        if not file_path:
            self.save_label.config(text="Please select a video file")
            return

        # Load video using moviepy
        video = VideoFileClip(file_path)

        # Reverse video
        reversed_video = video.fl_time(lambda t: video.duration - t)

        # Save reversed video
        save_path = file_path.split('.')[0] + "_reversed.mp4"
        reversed_video.write_videofile(save_path)

        self.save_label.config(text="Reversed video saved as: " + save_path)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    video_reverser = VideoReverser()
    video_reverser.run()