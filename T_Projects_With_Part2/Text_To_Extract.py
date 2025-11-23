from PIL import Image
import pytesseract as pt
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

class ImageToText:
    def __init__(self):
        self.current_location = os.getcwd() + '\\'
        self.tesseract_path = self.get_tesseract_path()

    def get_tesseract_path(self):
        try:
            return pt.pytesseract.tesseract_cmd
        except AttributeError:
            return input("Enter the Path to Tesseract: ")

    def extract(self, image_path, destination_path):
        try:
            pt.pytesseract.tesseract_cmd = self.tesseract_path
            for imageName in os.listdir(image_path):
                inputPath = os.path.join(image_path, imageName)
                img = Image.open(inputPath)
                text = pt.image_to_string(img, lang="eng")
                img_file = Path(inputPath).stem
                text_file = img_file + ".txt"
                output_path = os.path.join(destination_path, text_file)
                with open(output_path, "w") as file:
                    file.write(text)
            messagebox.showinfo("Success", "Text extracted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    root.title("Image to Text")

    image_to_text = ImageToText()

    tk.Label(root, text="Select Image Folder:").pack()
    image_path = tk.StringVar()
    tk.Entry(root, textvariable=image_path, width=50).pack()
    tk.Button(root, text="Browse", command=lambda: image_path.set(filedialog.askdirectory())).pack()

    tk.Label(root, text="Select Destination Folder:").pack()
    destination_path = tk.StringVar()
    tk.Entry(root, textvariable=destination_path, width=50).pack()
    tk.Button(root, text="Browse", command=lambda: destination_path.set(filedialog.askdirectory())).pack()

    def start_extraction():
        if image_path.get() and destination_path.get():
            image_to_text.extract(image_path.get(), destination_path.get())
        else:
            messagebox.showerror("Error", "Please select both image and destination folders!")

    tk.Button(root, text="Start Extraction", command=start_extraction).pack()

    root.mainloop()

if __name__ == "__main__":
    main()