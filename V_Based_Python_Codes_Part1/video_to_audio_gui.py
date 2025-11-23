import tkinter as tk
from tkinter import filedialog
from moviepy.editor import *

class VideoToAudio:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Video to Audio Converter")

        # Create GUI elements
        self.file_label = tk.Label(self.window, text="Select a video file:")
        self.file_label.pack()

        self.file_entry = tk.Entry(self.window, width=50)
        self.file_entry.pack()

        self.browse_button = tk.Button(self.window, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.format_label = tk.Label(self.window, text="Select audio format:")
        self.format_label.pack()

        self.format_var = tk.StringVar(self.window)
        self.format_var.set(".mp3")  # default value
        self.format_option = tk.OptionMenu(self.window, self.format_var, ".mp3", ".wav", ".ogg")
        self.format_option.pack()

        self.convert_button = tk.Button(self.window, text="Convert to Audio", command=self.convert_to_audio)
        self.convert_button.pack()

        self.save_label = tk.Label(self.window, text="")
        self.save_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4 .avi .mov")])
        self.file_entry.insert(0, file_path)

    def convert_to_audio(self):
        file_path = self.file_entry.get()
        if not file_path:
            self.save_label.config(text="Please select a video file")
            return

        # Get selected audio format
        audio_format = self.format_var.get()

        try:
            # Load video using moviepy
            video = VideoFileClip(file_path)

            # Extract audio
            audio = video.audio

            # Save audio
            save_path = file_path.split('.')[0] + audio_format
            audio.write_audiofile(save_path)

            self.save_label.config(text="Audio saved as: " + save_path)
        except Exception as e:
            self.save_label.config(text="Error: " + str(e))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    video_to_audio = VideoToAudio()
    video_to_audio.run()