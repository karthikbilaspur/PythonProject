import cv2
import tkinter as tk
from tkinter.filedialog import *

class ImageBorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Borders on images")
        self.root.geometry('320x220')
        self.img = None

        label = tk.Label(root, text="Select an image and then choose an option")
        label.grid(row=0, column=0, columnspan=2)

        tk.Button(root, text="Choose image", command=self.choose_image).grid(row=1, column=0, columnspan=2)

        self.border_type = tk.StringVar()
        self.border_type.set("constant")

        tk.Radiobutton(root, text='Constant border', variable=self.border_type, value="constant").grid(row=2, column=0)
        tk.Radiobutton(root, text='Reflection border', variable=self.border_type, value="reflection").grid(row=3, column=0)
        tk.Radiobutton(root, text='Default border', variable=self.border_type, value="default").grid(row=4, column=0)
        tk.Radiobutton(root, text='Replicate border', variable=self.border_type, value="replicate").grid(row=5, column=0)
        tk.Radiobutton(root, text='Wrap border', variable=self.border_type, value="wrap").grid(row=6, column=0)

        tk.Button(root, text="Apply border", command=self.apply_border).grid(row=7, column=0, columnspan=2)

    def choose_image(self):
        photo = askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if photo:
            self.img = cv2.imread(photo)
            self.img = cv2.resize(self.img, (500, 500))

    def apply_border(self):
        if self.img is None:
            return

        border_type = self.border_type.get()
        if border_type == "constant":
            bordered = cv2.copyMakeBorder(self.img, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
        elif border_type == "reflection":
            bordered = cv2.copyMakeBorder(self.img, 50, 50, 50, 50, cv2.BORDER_REFLECT)
        elif border_type == "default":
            bordered = cv2.copyMakeBorder(self.img, 50, 50, 50, 50, cv2.BORDER_DEFAULT)
        elif border_type == "replicate":
            bordered = cv2.copyMakeBorder(self.img, 50, 50, 50, 50, cv2.BORDER_REPLICATE)
        elif border_type == "wrap":
            bordered = cv2.copyMakeBorder(self.img, 50, 50, 50, 50, cv2.BORDER_WRAP)

        cv2.imshow("Bordered Image", bordered)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBorderApp(root)
    root.mainloop()