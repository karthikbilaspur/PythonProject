from pytube import YouTube
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class YouTubeDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Downloader")

        # Create frames
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)

        # Create labels and entries
        self.url_label = tk.Label(self.frame1, text="YouTube URL:")
        self.url_entry = tk.Entry(self.frame1, width=50)
        self.path_label = tk.Label(self.frame2, text="Download Path:")
        self.path_entry = tk.Entry(self.frame2, width=50)
        self.path_button = tk.Button(self.frame2, text="Browse", command=self.browse_path)

        # Create radio buttons
        self.download_type = tk.StringVar()
        self.download_type.set("video")
        self.video_radio = tk.Radiobutton(self.frame3, text="Video", variable=self.download_type, value="video")
        self.audio_radio = tk.Radiobutton(self.frame3, text="Audio", variable=self.download_type, value="audio")

        # Create buttons
        self.download_button = tk.Button(self.frame3, text="Download", command=self.download)

        # Layout frames and widgets
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.url_label.pack(side=tk.LEFT)
        self.url_entry.pack(side=tk.LEFT)
        self.path_label.pack(side=tk.LEFT)
        self.path_entry.pack(side=tk.LEFT)
        self.path_button.pack(side=tk.LEFT)
        self.video_radio.pack(side=tk.LEFT)
        self.audio_radio.pack(side=tk.LEFT)
        self.download_button.pack(side=tk.LEFT)

    def browse_path(self):
        path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def download(self):
        url = self.url_entry.get()
        path = self.path_entry.get()
        download_type = self.download_type.get()

        if not url or not path:
            messagebox.showerror("Error", "Please enter URL and path.")
            return

        try:
            yt = YouTube(url)
            if download_type == "video":
                stream = yt.streams.get_highest_resolution()
                if stream:
                    print(f"Downloading {yt.title}...")
                    stream.download(path)
                    print("Download complete!")
                else:
                    print("No video stream found.")
            elif download_type == "audio":
                stream = yt.streams.get_audio_only()
                if stream:
                    print(f"Downloading {yt.title}...")
                    stream.download(path)
                    print("Download complete!")
                else:
                    print("No audio stream found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    downloader = YouTubeDownloader()
    downloader.run()