import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class MemeGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Random Meme Generator")

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.button = tk.Button(self.root, text="Get Random Meme", command=self.get_meme)
        self.button.pack()

        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.pack()

        self.get_meme()

    def get_meme(self):
        try:
            response = requests.get("https://meme-api.herokuapp.com/gimme")
            response.raise_for_status()
            data = response.json()
            self.meme_url = data["url"]

            response = requests.get(self.meme_url)
            response.raise_for_status()
            image_data = response.content

            image = Image.open(BytesIO(image_data))
            image.thumbnail((400, 400))  # Resize the image to fit the window
            image = ImageTk.PhotoImage(image)

            self.image_label.config(image=image)
            self.image_label.image = image  # Keep a reference to prevent garbage collection
            self.error_label.config(text="")
        except requests.exceptions.RequestException as e:
            self.error_label.config(text="Error: " + str(e))
            self.image_label.config(image=None)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    generator = MemeGenerator()
    generator.run()