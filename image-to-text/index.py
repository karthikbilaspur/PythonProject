from PIL import Image
import pytesseract as pt
import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable, cast

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}

class ImageToText:
    def __init__(self):
        # Find tesseract automatically, don't ask via input() in a GUI
        self.tesseract_path = shutil.which("tesseract")
        if self.tesseract_path:
            pt.pytesseract.tesseract_cmd = self.tesseract_path

    def extract(self, image_path: str, destination_path: str) -> None:
        if not self.tesseract_path:
            raise RuntimeError(
                "Tesseract not found on this computer.\n"
                "Install it from https://github.com/tesseract-ocr/tesseract "
                "and make sure 'tesseract' is in PATH, then restart the app."
            )
        os.makedirs(destination_path, exist_ok=True)
        files = [f for f in os.listdir(image_path) if Path(f).suffix.lower() in IMAGE_EXTS]
        if not files:
            raise FileNotFoundError("No image files found in that folder.")
        for image_name in files:
            input_path = os.path.join(image_path, image_name)
            img = Image.open(input_path)
            image_to_string = cast(Callable[..., str], getattr(pt, "image_to_string"))
            text = image_to_string(img, lang="eng")
            out_path = os.path.join(destination_path, Path(input_path).stem + ".txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)

def main():
    root = tk.Tk()
    root.title("Image to Text")
    root.geometry("520x320")

    tk.Label(root, text="Select Image Folder:").pack(pady=5)
    image_path = tk.StringVar()
    tk.Entry(root, textvariable=image_path, width=50).pack()
    tk.Button(root, text="Browse", command=lambda: image_path.set(filedialog.askdirectory())).pack(pady=3)

    tk.Label(root, text="Select Destination Folder:").pack(pady=5)
    destination_path = tk.StringVar()
    tk.Entry(root, textvariable=destination_path, width=50).pack()
    tk.Button(root, text="Browse", command=lambda: destination_path.set(filedialog.askdirectory())).pack(pady=3)

    def start_extraction():
        if not image_path.get() or not destination_path.get():
            messagebox.showerror("Error", "Please select both image and destination folders!")
            return
        try:
            ImageToText().extract(image_path.get(), destination_path.get())
            messagebox.showinfo("Success", "Text extracted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Start Extraction", command=start_extraction).pack(pady=15)
    root.mainloop()

if __name__ == "__main__":
    main()
