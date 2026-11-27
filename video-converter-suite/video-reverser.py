import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import VideoFileClip  # type: ignore[reportMissingTypeStubs]
from typing import Any, Callable, cast
import os

class VideoReverser:
    def __init__(self, parent: tk.Misc | None = None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Video Reverser")
        self.window.geometry("450x220")
        tk.Label(self.window, text="Select a video file:", font=("Arial", 11, "bold")).pack(pady=10)
        self.file_entry = tk.Entry(self.window, width=55)
        self.file_entry.pack(padx=10)
        tk.Button(self.window, text="Browse", command=self.browse_file).pack(pady=5)
        tk.Button(self.window, text="Reverse Video", bg="#2196F3", fg="white", command=self.reverse_video).pack(pady=5)
        self.save_label = tk.Label(self.window, text="", wraplength=400, fg="green")
        self.save_label.pack(pady=5)

    def browse_file(self):
        p = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
        if p:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, p)

    def reverse_video(self):
        file_path = self.file_entry.get().strip()
        if not file_path:
            messagebox.showwarning("Missing", "Please select a video file")
            return
        try:
            self.save_label.config(text="Reversing... please wait")
            self.window.update()
            video = cast(Any, VideoFileClip(file_path))
            # MoviePy v2 uses time_transform; retain compatibility with v1.
            duration = cast(float, getattr(video, "duration"))
            transform = getattr(video, "time_transform", None)
            if not callable(transform):
                transform = getattr(video, "fl_time")
            time_transform = cast(
                Callable[[Callable[[float], float]], Any], transform
            )
            reversed_video = time_transform(lambda t: duration - t)
            save_path = os.path.splitext(file_path)[0] + "_reversed.mp4"
            reversed_video.write_videofile(save_path, logger=None)
            video.close(); reversed_video.close()
            self.save_label.config(text="Saved as: " + save_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.save_label.config(text="Error: " + str(e))

    def run(self):
        self.window.mainloop()

def open_window(parent: tk.Misc | None = None):
    return VideoReverser(parent)

if __name__ == "__main__":
    VideoReverser().run()
