import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
from typing import Any


class ImageToolkit:
    def __init__(self, root: Any) -> None:
        self.root = root
        self.root.title("Image Toolkit - All in One")
        self.root.geometry("900x600")
        self.img: np.ndarray[Any, Any] | None = None
        self.original: np.ndarray[Any, Any] | None = None
        self.display_img: ImageTk.PhotoImage | None = None

        # --- Top controls ---
        top = tk.Frame(root)
        top.pack(pady=10)

        tk.Button(top, text="Open Image", command=self.open_image).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Save as PDF", command=self.save_pdf).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="ASCII Art", command=self.make_ascii).pack(side=tk.LEFT, padx=5)

        # --- Middle: image + tools ---
        mid = tk.Frame(root)
        mid.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(mid, text="Open an image to start", bg="#eee", width=70, height=25)
        self.label.pack(side=tk.LEFT, padx=10, pady=10)

        tools = tk.Frame(mid)
        tools.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

        tk.Label(tools, text="--- Adjust ---", font=("Arial", 11, "bold")).pack(pady=5)
        tk.Label(tools, text="Contrast (1.0 - 3.0)").pack()
        self.contrast_var = tk.DoubleVar(value=1.5)
        tk.Scale(tools, from_=1.0, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.contrast_var).pack()
        tk.Button(tools, text="Apply Contrast", command=self.apply_contrast).pack(pady=3)

        tk.Label(tools, text="--- Filters ---", font=("Arial", 11, "bold")).pack(pady=5)
        for name, cmd in [
            ("Grayscale", self.to_grayscale),
            ("Blur", self.to_blur),
            ("Edge Detection", self.to_edges),
            ("Sketch", self.to_sketch),
        ]:
            tk.Button(tools, text=name, width=20, command=cmd).pack(pady=2)

        tk.Label(tools, text="--- Transform ---", font=("Arial", 11, "bold")).pack(pady=5)
        tk.Button(tools, text="Rotate 90°", width=20, command=self.rotate).pack(pady=2)
        tk.Button(tools, text="Flip Horizontal", width=20, command=self.flip).pack(pady=2)
        tk.Button(tools, text="Resize to 800x600", width=20, command=self.resize).pack(pady=2)

        tk.Label(tools, text="--- Border ---", font=("Arial", 11, "bold")).pack(pady=5)
        self.border_type = ttk.Combobox(tools, values=["constant", "reflection", "replicate", "wrap", "default"])
        self.border_type.current(0)
        self.border_type.pack()
        tk.Button(tools, text="Add Border (50px)", width=20, command=self.add_border).pack(pady=2)

        tk.Label(tools, text="--- Color Detect ---", font=("Arial", 11, "bold")).pack(pady=5)
        self.color_var = ttk.Combobox(tools, values=["red", "green", "blue"])
        self.color_var.current(0)
        self.color_var.pack()
        tk.Button(tools, text="Detect Color", width=20, command=self.detect_color).pack(pady=2)

    # ---------- Core ----------
    def open_image(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if not path:
            return

        loaded = cv2.imread(path, cv2.IMREAD_COLOR)
        if loaded is None:
            messagebox.showerror("Open Image", "Could not load the selected image.")
            return

        self.img = loaded
        self.original = loaded.copy()
        self.show(self.img)

    def show(self, img: np.ndarray[Any, Any]) -> None:
        # Convert BGR -> RGB for Tkinter
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        pil.thumbnail((600, 500))
        self.display_img = ImageTk.PhotoImage(pil)
        self.label.config(image=self.display_img, text="")

    def reset(self) -> None:
        if self.original is not None:
            self.img = self.original.copy()
            self.show(self.img)

    def save_image(self) -> None:
        if self.img is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if path:
            cv2.imwrite(path, self.img)
            messagebox.showinfo("Saved", f"Saved to {path}")

    def save_pdf(self) -> None:
        if self.img is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if path:
            rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            Image.fromarray(rgb).save(path, "PDF", resolution=100.0)
            messagebox.showinfo("Saved", "PDF saved!")

    # ---------- Adjust / Filters ----------
    def apply_contrast(self) -> None:
        if self.img is None:
            return
        alpha = float(self.contrast_var.get())
        ycrcb = cv2.cvtColor(self.img, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)
        y = cv2.convertScaleAbs(y, alpha=alpha, beta=0)
        self.img = cv2.cvtColor(cv2.merge([y, cr, cb]), cv2.COLOR_YCrCb2BGR)
        self.show(self.img)

    def to_grayscale(self) -> None:
        if self.img is None:
            return
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self.show(self.img)

    def to_blur(self) -> None:
        if self.img is None:
            return
        self.img = cv2.GaussianBlur(self.img, (5, 5), 0)
        self.show(self.img)

    def to_edges(self) -> None:
        if self.img is None:
            return
        edges = cv2.Canny(self.img, 100, 200)
        self.img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self.show(self.img)

    def to_sketch(self) -> None:
        if self.img is None:
            return
        gray = np.asarray(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY), dtype=np.uint8)
        inv = np.asarray(255 - gray, dtype=np.uint8)
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        self.img = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
        self.show(self.img)

    # ---------- Transform / Border ----------
    def rotate(self) -> None:
        if self.img is None:
            return
        self.img = cv2.rotate(self.img, cv2.ROTATE_90_CLOCKWISE)
        self.show(self.img)

    def flip(self) -> None:
        if self.img is None:
            return
        self.img = cv2.flip(self.img, 1)
        self.show(self.img)

    def resize(self) -> None:
        if self.img is None:
            return
        self.img = cv2.resize(self.img, (800, 600))
        self.show(self.img)

    def add_border(self) -> None:
        if self.img is None:
            return
        types = {
            "constant": cv2.BORDER_CONSTANT,
            "reflection": cv2.BORDER_REFLECT,
            "replicate": cv2.BORDER_REPLICATE,
            "wrap": cv2.BORDER_WRAP,
            "default": cv2.BORDER_DEFAULT,
        }
        self.img = cv2.copyMakeBorder(self.img, 50, 50, 50, 50, types[self.border_type.get()])
        self.show(self.img)

    # ---------- Color Detect ----------
    def detect_color(self) -> None:
        if self.img is None:
            return
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        color = self.color_var.get()
        if color == "red":
            m1 = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
            m2 = cv2.inRange(hsv, np.array([160, 100, 100]), np.array([179, 255, 255]))
            mask = cv2.bitwise_or(m1, m2)
        elif color == "green":
            mask = cv2.inRange(hsv, np.array([40, 40, 40]), np.array([80, 255, 255]))
        else:
            mask = cv2.inRange(hsv, np.array([100, 50, 50]), np.array([130, 255, 255]))
        self.img = cv2.bitwise_and(self.img, self.img, mask=mask)
        self.show(self.img)

    # ---------- ASCII ----------
    def make_ascii(self) -> None:
        if self.img is None:
            return
        chars = "@%#*+=-:. "
        gray: np.ndarray[Any, np.dtype[np.uint8]] = np.asarray(
            cv2.resize(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY), (80, 40)),
            dtype=np.uint8,
        )
        out = ""
        for row in gray:
            for pixel in row:
                normalized = float(pixel) / 255.0
                index = int((len(chars) - 1) * (1.0 - normalized))
                out += chars[max(0, min(len(chars) - 1, index))]
            out += "\n"
        top = tk.Toplevel(self.root)
        top.title("ASCII Art")
        txt = tk.Text(top, font=("Courier", 8), width=90, height=45)
        txt.pack()
        txt.insert("1.0", out)
        with open("ascii_art.txt", "w", encoding="utf-8") as f:
            f.write(out)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToolkit(root)
    root.mainloop()