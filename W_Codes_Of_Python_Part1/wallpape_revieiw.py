import tkinter as tk
from pexels_api import API
import requests
from PIL import Image, ImageTk
from io import BytesIO
import random

# Set up Pexels API
PEXELS_API_KEY = 'YOUR_API_KEY'
api = API(PEXELS_API_KEY)

class WallpaperViewer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Wallpaper Viewer")
        self.photos = []
        self.current_photo = 0

        self.fetch_button = tk.Button(root, text="Fetch Wallpaper", command=self.fetch_wallpaper)
        self.fetch_button.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.next_button = tk.Button(root, text="Next", command=self.next_wallpaper)
        self.next_button.pack()

        self.prev_button = tk.Button(root, text="Previous", command=self.prev_wallpaper)
        self.prev_button.pack()

    def fetch_wallpaper(self):
        self.photos = api.photos.search('nature', per_page=10)['photos']
        self.display_wallpaper()

    def display_wallpaper(self):
        if self.photos:
            photo = self.photos[self.current_photo]
            url = photo['src']['original']
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.thumbnail((800, 600))  # Resize image
            photo_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo_image)
            self.image_label.image = photo_image  # Keep a reference to prevent garbage collection

    def next_wallpaper(self):
        if self.photos:
            self.current_photo = (self.current_photo + 1) % len(self.photos)
            self.display_wallpaper()

    def prev_wallpaper(self):
        if self.photos:
            self.current_photo = (self.current_photo - 1) % len(self.photos)
            self.display_wallpaper()

if __name__ == "__main__":
    root = tk.Tk()
    app = WallpaperViewer(root)
    root.mainloop()