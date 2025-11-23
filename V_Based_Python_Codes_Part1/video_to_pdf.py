import tkinter as tk
from tkinter import filedialog
import cv2
from moviepy.editor import *
from PIL import Image
from pdf2image import convert_from_path
import os

class VideoToPdf:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Video to PDF")

        # Create GUI elements
        self.file_label = tk.Label(self.window, text="Select a video file:")
        self.file_label.pack()

        self.file_entry = tk.Entry(self.window, width=50)
        self.file_entry.pack()

        self.browse_button = tk.Button(self.window, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.convert_button = tk.Button(self.window, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_button.pack()

        self.save_label = tk.Label(self.window, text="")
        self.save_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4 .avi .mov")])
        self.file_entry.insert(0, file_path)

    def convert_to_pdf(self):
        file_path = self.file_entry.get()
        if not file_path:
            self.save_label.config(text="Please select a video file")
            return

        # Load video using moviepy
        video = VideoFileClip(file_path)

        # Extract frames
        frames = []
        for i, frame in enumerate(video.iter_frames()):
            img = Image.fromarray(frame)
            frames.append(img)

        # Save frames as PDF
        save_path = file_path.split('.')[0] + ".pdf"
        frames[0].save(save_path, save_all=True, append_images=frames[1:])

        self.save_label.config(text="PDF saved as: " + save_path)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    video_to_pdf = VideoToPdf()
    video_to_pdf.run()