import tkinter as tk
from tkinter import filedialog
from pygame import mixer

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Music Player")
        self.track = tk.StringVar()
        self.status = tk.StringVar()
        self.playlist = []

        # Initialize Pygame mixer
        mixer.init()

        # Create GUI widgets
        self.track_label = tk.Label(root, textvariable=self.track)
        self.track_label.pack()
        self.status_label = tk.Label(root, textvariable=self.status)
        self.status_label.pack()
        self.play_button = tk.Button(root, text="Play", command=self.play_music)
        self.play_button.pack()
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_music)
        self.pause_button.pack()
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_music)
        self.stop_button.pack()
        self.open_button = tk.Button(root, text="Open", command=self.open_music_file)
        self.open_button.pack()
        self.playlist_button = tk.Button(root, text="Playlist", command=self.show_playlist)
        self.playlist_button.pack()

    def show_playlist(self):
        # Create a new window to display the playlist
        playlist_window = tk.Toplevel(self.root)
        playlist_window.title("Playlist")
        playlist_listbox = tk.Listbox(playlist_window)
        for track in self.playlist:
            playlist_listbox.insert(tk.END, track)
        playlist_listbox.pack()

    def open_music_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        self.track.set(file_path)
        self.playlist.append(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()