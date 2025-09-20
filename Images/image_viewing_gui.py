import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.image_path = None
        self.image = None
        self.photo = None

        self.create_widgets()

    def create_widgets(self):
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)

        self.open_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        self.open_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=10)

    def open_image(self):
        self.image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", ".png .jpg .jpeg .bmp")])

        if self.image_path:
            self.image = Image.open(self.image_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

    def save_image(self):
        if self.image_path:
            save_path = filedialog.asksaveasfilename(title="Save Image", defaultextension=".png", filetypes=[("PNG Image", ".png")])
            if save_path:
                self.image.save(save_path)

if __name__ == "__main__":
    root = tk.Tk()
    viewer = ImageViewer(root)
    root.mainloop()