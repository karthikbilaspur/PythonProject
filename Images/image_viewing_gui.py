import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.image_path = None
        self.image = None
        self.photo = None
        self.history = []

        self.create_widgets()

    def create_widgets(self):
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)

        self.open_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        self.open_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=10)

        self.edit_frame = tk.Frame(self.root)
        self.edit_frame.pack(pady=10)

        self.rotate_button = tk.Button(self.edit_frame, text="Rotate 90°", command=self.rotate_image)
        self.rotate_button.pack(side=tk.LEFT, padx=5)

        self.flip_button = tk.Button(self.edit_frame, text="Flip Horizontal", command=self.flip_image)
        self.flip_button.pack(side=tk.LEFT, padx=5)

        self.grayscale_button = tk.Button(self.edit_frame, text="Grayscale", command=self.grayscale_image)
        self.grayscale_button.pack(side=tk.LEFT, padx=5)

        self.enhance_button = tk.Button(self.edit_frame, text="Enhance", command=self.enhance_image)
        self.enhance_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(self.edit_frame, text="Undo", command=self.undo_image)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack(pady=10)

    def open_image(self):
        self.image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", ".png .jpg .jpeg .bmp")])

        if self.image_path:
            self.image = Image.open(self.image_path)
            self.history.append(self.image.copy())
            self.display_image()
            self.display_info()

    def display_image(self):
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.photo)
        self.image_label.image = self.photo

    def display_info(self):
        width, height = self.image.size
        self.info_label.config(text=f"Image Size: {width}x{height}")

    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(title="Save Image", defaultextension=".png", filetypes=[("PNG Image", ".png"), ("JPEG Image", ".jpg"), ("BMP Image", ".bmp")])
            if save_path:
                self.image.save(save_path)

    def rotate_image(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
            self.history.append(self.image.copy())
            self.display_image()

    def flip_image(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.history.append(self.image.copy())
            self.display_image()

    def grayscale_image(self):
        if self.image:
            self.image = self.image.convert('L').convert('RGB')
            self.history.append(self.image.copy())
            self.display_image()

    def enhance_image(self):
        if self.image:
            enhancer = ImageEnhance.Sharpness(self.image)
            self.image = enhancer.enhance(1.5)
            self.history.append(self.image.copy())
            self.display_image()

    def undo_image(self):
        if len(self.history) > 1:
            self.history.pop()
            self.image = self.history[-1].copy()
            self.display_image()

if __name__ == "__main__":
    root = tk.Tk()
    viewer = ImageViewer(root)
    root.mainloop()

    