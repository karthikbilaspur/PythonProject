import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import VideoFileClip  # type: ignore[reportMissingTypeStubs]
import os, sys

def convert_video_to_audio(video_file: str, audio_format: str) -> str:
    """CLI / reusable function: video -> audio"""
    video = VideoFileClip(video_file)
    if video.audio is None:
        video.close()
        raise ValueError("This video has no audio track")
    audio = video.audio
    audio_file = os.path.splitext(video_file)[0] + audio_format
    audio.write_audiofile(audio_file, logger=None)
    video.close(); audio.close()
    return audio_file

class VideoToAudio:
    def __init__(self, parent: tk.Misc | None = None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Video to Audio Converter")
        self.window.geometry("450x280")
        tk.Label(self.window, text="Select a video file:", font=("Arial", 11, "bold")).pack(pady=10)
        self.file_entry = tk.Entry(self.window, width=55)
        self.file_entry.pack(padx=10)
        tk.Button(self.window, text="Browse", command=self.browse_file).pack(pady=5)
        tk.Label(self.window, text="Select audio format:").pack(pady=5)
        self.format_var = tk.StringVar(self.window)
        self.format_var.set(".mp3")
        tk.OptionMenu(self.window, self.format_var, ".mp3", ".wav", ".ogg").pack()
        tk.Button(self.window, text="Convert to Audio", bg="#4CAF50", fg="white", command=self.convert_to_audio).pack(pady=10)
        self.save_label = tk.Label(self.window, text="", wraplength=400, fg="green")
        self.save_label.pack()

    def browse_file(self):
        p = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
        if p:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, p)

    def convert_to_audio(self):
        file_path = self.file_entry.get().strip()
        if not file_path:
            messagebox.showwarning("Missing", "Please select a video file")
            return
        try:
            self.save_label.config(text="Converting... please wait")
            self.window.update()
            save_path = convert_video_to_audio(file_path, self.format_var.get())
            self.save_label.config(text="Audio saved as: " + save_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.save_label.config(text="Error: " + str(e))

    def run(self):
        self.window.mainloop()

def open_window(parent: tk.Misc | None = None):
    return VideoToAudio(parent)

def main_cli():
    video_file = input("Enter the path to the video file: ").strip()
    audio_format = input("Enter format (.mp3 / .wav / .ogg): ").strip()
    if not audio_format.startswith("."):
        audio_format = "." + audio_format
    try:
        out = convert_video_to_audio(video_file, audio_format)
        print(f"Audio saved as: {out}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # GUI if run directly, CLI if args given: python video_to_audio.py --cli
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        main_cli()
    else:
        VideoToAudio().run()
