import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab
import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip
import threading

class TextExtractor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real-time Text Extraction")
        self.label = tk.Label(self.root, text="Extracted Text:")
        self.label.pack()
        self.text_box = tk.Text(self.root, width=80, height=20)
        self.text_box.pack()

        # Create buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()
        self.save_button = tk.Button(self.button_frame, text="Save to File", command=self.save_text_to_file)
        self.save_button.pack(side=tk.LEFT)
        self.copy_button = tk.Button(self.button_frame, text="Copy to Clipboard", command=self.copy_text_to_clipboard)
        self.copy_button.pack(side=tk.LEFT)

        # Create OCR engine configuration options
        self.ocr_frame = tk.Frame(self.root)
        self.ocr_frame.pack()
        self.lang_label = tk.Label(self.ocr_frame, text="Language:")
        self.lang_label.pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(self.root)
        self.lang_var.set("eng")  # default value
        self.lang_option = tk.OptionMenu(self.ocr_frame, self.lang_var, "eng", "spa", "fra")
        self.lang_option.pack(side=tk.LEFT)

        # Start image capture and text extraction thread
        self.capture_thread = threading.Thread(target=self.capture_and_extract_text)
        self.capture_thread.start()

    def capture_and_extract_text(self):
        while True:
            try:
                # Capture the screen
                img = ImageGrab.grab(bbox=(100, 100, 700, 500))  # adjust the bbox to capture the desired region
                img = np.array(img)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                # Extract text from the image
                text = pytesseract.image_to_string(img, lang=self.lang_var.get())

                # Update the text box
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_text_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.text_box.get(1.0, tk.END))

    def copy_text_to_clipboard(self):
        pyperclip.copy(self.text_box.get(1.0, tk.END))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    extractor = TextExtractor()
    extractor.run()