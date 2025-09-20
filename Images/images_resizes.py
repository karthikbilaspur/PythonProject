import tkinter as tk
from tkinter import filedialog
from PIL import Image

class ImageResizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Resizer")

        tk.Label(self.root, text="Select an image file:").grid(row=0, column=0)
        self.image_path = tk.StringVar()
        tk.Entry(self.root, textvariable=self.image_path, width=50).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_image).grid(row=0, column=2)

        tk.Label(self.root, text="New width:").grid(row=1, column=0)
        self.new_width = tk.StringVar()
        tk.Entry(self.root, textvariable=self.new_width).grid(row=1, column=1)

        tk.Label(self.root, text="Output file path:").grid(row=2, column=0)
        self.output_path = tk.StringVar()
        tk.Entry(self.root, textvariable=self.output_path, width=50).grid(row=2, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(row=2, column=2)

        tk.Button(self.root, text="Resize", command=self.resize_image).grid(row=3, column=1)

    def browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        self.image_path.set(path)

    def browse_output(self):
        path = filedialog.asksaveasfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        self.output_path.set(path)

    def resize_image(self):
        try:
            img = Image.open(self.image_path.get())
            aspect_ratio = img.height / img.width
            new_height = int(aspect_ratio * int(self.new_width.get()))
            new_size = (int(self.new_width.get()), new_height)
            resized_img = img.resize(new_size)
            resized_img.save(self.output_path.get())
            tk.Label(self.root, text="Image resized and saved successfully.").grid(row=4, column=1)
        except Exception as e:
            tk.Label(self.root, text=f"Error resizing image: {e}").grid(row=4, column=1)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageResizer()
    app.run()