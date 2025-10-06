import cv2
import tkinter as tk
from tkinter import filedialog

class ImageBorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Border App")
        self.root.geometry('350x300')
        self.img = None
        self.border_size = 50

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.root, text="Select an image and choose a border option")
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        tk.Button(self.root, text="Choose image", command=self.choose_image).grid(row=1, column=0, columnspan=2)

        self.border_type = tk.StringVar()
        self.border_type.set("constant")

        border_types = [
            ("Constant border", "constant"),
            ("Reflection border", "reflection"),
            ("Default border", "default"),
            ("Replicate border", "replicate"),
            ("Wrap border", "wrap")
        ]

        for i, (text, value) in enumerate(border_types):
            tk.Radiobutton(self.root, text=text, variable=self.border_type, value=value).grid(row=i+2, column=0)

        tk.Button(self.root, text="Apply border", command=self.apply_border).grid(row=7, column=0, columnspan=2)

        # Add border size entry
        tk.Label(self.root, text="Border size").grid(row=8, column=0)
        self.border_size_entry = tk.Entry(self.root)
        self.border_size_entry.insert(0, str(self.border_size))
        self.border_size_entry.grid(row=8, column=1)

    def choose_image(self):
        photo = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if photo:
            self.img = cv2.imread(photo)
            self.img = cv2.resize(self.img, (500, 500))

    def apply_border(self):
        if self.img is None:
            return

        try:
            self.border_size = int(self.border_size_entry.get())
        except ValueError:
            print("Invalid border size")
            return

        border_type = self.border_type.get()
        border_types = {
            "constant": cv2.BORDER_CONSTANT,
            "reflection": cv2.BORDER_REFLECT,
            "default": cv2.BORDER_DEFAULT,
            "replicate": cv2.BORDER_REPLICATE,
            "wrap": cv2.BORDER_WRAP
        }

        bordered = cv2.copyMakeBorder(self.img, self.border_size, self.border_size, self.border_size, self.border_size, border_types[border_type])

        cv2.imshow("Bordered Image", bordered)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBorderApp(root)
    root.mainloop()