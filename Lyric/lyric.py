import requests
import tkinter as tk
from tkinter import messagebox

class LyricFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Lyric Finder")
        self.root.geometry("800x600")

        self.artist_label = tk.Label(root, text="Artist Name:")
        self.artist_label.pack()
        self.artist_entry = tk.Entry(root, width=50)
        self.artist_entry.pack()

        self.title_label = tk.Label(root, text="Song Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(root, width=50)
        self.title_entry.pack()

        self.find_button = tk.Button(root, text="Find Lyrics", command=self.find_lyrics)
        self.find_button.pack()

        self.lyrics_text = tk.Text(root, height=20, width=80)
        self.lyrics_text.pack()

    def find_lyrics(self):
        artist = self.artist_entry.get()
        title = self.title_entry.get()

        if not artist or not title:
            messagebox.showerror("Error", "Please enter both artist and title")
            return

        base_url = f'https://api.lyrics.ovh/v1/{artist}/{title}'
        try:
            response = requests.get(base_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))
            return

        data = response.json()
        lyrics = data.get('lyrics', 'Lyrics not found for this song.')

        self.lyrics_text.delete(1.0, tk.END)
        self.lyrics_text.insert(tk.END, lyrics)

if __name__ == "__main__":
    root = tk.Tk()
    app = LyricFinder(root)
    root.mainloop()