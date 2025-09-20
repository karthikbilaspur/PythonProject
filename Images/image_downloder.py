import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os
from datetime import datetime

class ImageDownloader:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Downloader")

        # URL entry
        self.url_label = tk.Label(self.window, text="Image URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.window, width=50)
        self.url_entry.pack()

        tk.Button(self.window, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        # Download button
        self.download_button = tk.Button(self.window, text="Download", command=self.download_image)
        self.download_button.pack()

        # Image preview
        self.image_label = tk.Label(self.window)
        self.image_label.pack()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.dir_entry = tk.Entry(self.window, width=50)
        self.dir_entry.pack()
        self.dir_entry.insert(0, directory)

    def download_image(self):
        url = self.url_entry.get()
        try:
            directory = self.dir_entry.get()
        except AttributeError:
            messagebox.showerror("Error", "Please select a directory")
            return
        if not url or not directory:
            messagebox.showerror("Error", "Please enter both URL and directory")
            return
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Directory does not exist")
            return
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))
            return
        try:
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            messagebox.showerror("Error", "Failed to open image")
            return
        filename = f"image_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        try:
            image.save(os.path.join(directory, filename))
            messagebox.showinfo("Success", "Image downloaded successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    downloader = ImageDownloader()
    downloader.run()