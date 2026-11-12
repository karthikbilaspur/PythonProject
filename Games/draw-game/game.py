import os
from typing import Any

import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageTk
import matplotlib
matplotlib.use("Agg")

# --- Try to import TF lazily so UI can show errors nicely ---
tf: Any = None
keras: Any = None
has_tf = False
try:
    import tensorflow as tf  # type: ignore[import-not-found]
    keras = tf.keras
    has_tf = True
except ImportError:
    has_tf = False

HAS_TF = has_tf
MODEL_PATH = "mnist_model.keras"
CANVAS_SIZE = 280
IMG_SIZE = 28

# ---------- Model ----------
def get_model() -> Any:
    """Load saved model, or train a new one if missing."""
    if os.path.exists(MODEL_PATH):
        print(f"Loading model from {MODEL_PATH}...")
        return keras.models.load_model(MODEL_PATH)

    print("No saved model — training (one time, ~30s)...")
    (X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
    X_train = X_train.astype("float32") / 255.0
    X_test = X_test.astype("float32") / 255.0

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    model.fit(X_train, y_train, epochs=5,
              validation_data=(X_test, y_test), verbose=1)
    model.save(MODEL_PATH)
    print(f"Saved to {MODEL_PATH}")
    return model

# ---------- MNIST-style preprocessing (the important fix) ----------
def preprocess_canvas(pil_img: Image.Image) -> np.ndarray[Any, np.dtype[np.float32]]:
    """
    Convert 280x280 white-bg drawing -> 28x28 MNIST-style array.
    MNIST = white digit (1.0) on black bg (0.0), centered by mass.
    """
    # 1. Invert: drawing was black on white, MNIST is white on black
    arr = 255 - np.array(pil_img.convert("L"))  # now digit = bright

    # 2. If blank, return zeros
    if arr.max() == 0:
        return np.zeros((28, 28), dtype=np.float32)

    # 3. Crop to bounding box
    ys, xs = np.where(arr > 20)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cropped = arr[y0:y1+1, x0:x1+1]

    # 4. Resize longest side to 20, keep aspect ratio (like MNIST)
    h, w = cropped.shape
    scale = 20.0 / max(h, w)
    new_h, new_w = max(1, int(round(h * scale))), max(1, int(round(w * scale)))
    resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.LANCZOS)
    resized = np.array(Image.fromarray(cropped).resize((new_w, new_h), resample))

    # 5. Pad to 28x28
    canvas = np.zeros((28, 28), dtype=np.float32)
    y_off = (28 - new_h) // 2
    x_off = (28 - new_w) // 2
    canvas[y_off:y_off+new_h, x_off:x_off+new_w] = resized

    # 6. Center by center-of-mass (MNIST does this)
    cy, cx = np.array(np.where(canvas > 0)).mean(axis=1)
    shift_y = int(round(14 - cy))
    shift_x = int(round(14 - cx))
    canvas = np.roll(canvas, shift=(shift_y, shift_x), axis=(0, 1))

    return (canvas / 255.0).astype(np.float32)

# ---------- App ----------
Point = tuple[int, int]
Stroke = list[Point]


class DrawingApp:
    def __init__(self, root: tk.Tk, model: Any):
        self.root = root
        self.model = model
        self.root.title("✏️ AI Drawing Game — Draw a Digit")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.brush_size = tk.IntVar(value=14)
        self.eraser_on = False
        self.last_x: int | None = None
        self.last_y: int | None = None
        self.strokes: list[Stroke] = []
        self.current_stroke: Stroke = []

        # --- Layout ---
        main = tk.Frame(root, bg="#1e1e1e", padx=14, pady=14)
        main.pack()

        tk.Label(main, text="Draw a digit (0-9)", bg="#1e1e1e", fg="white",
                 font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        # Left: canvas
        canvas_frame = tk.Frame(main, bg="white", padx=2, pady=2)
        canvas_frame.grid(row=1, column=0, rowspan=3, padx=(0, 14))
        self.canvas = tk.Canvas(canvas_frame, width=CANVAS_SIZE, height=CANVAS_SIZE,
                                bg="white", highlightthickness=0, cursor="pencil")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_down)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_up)

        # Right: preview + predictions
        right = tk.Frame(main, bg="#1e1e1e")
        right.grid(row=1, column=1, sticky="n")

        tk.Label(right, text="What the AI sees (28×28)", bg="#1e1e1e", fg="#aaa",
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.preview_label = tk.Label(right, bg="black", width=112, height=112)
        self.preview_label.pack(pady=(2, 10))

        tk.Label(right, text="AI's Guesses", bg="#1e1e1e", fg="#aaa",
                 font=("Segoe UI", 9)).pack(anchor="w")

        self.pred_labels: list[tk.Label] = []
        self.pred_bars: list[tuple[tk.Frame, tk.Frame, tk.Label]] = []
        for _ in range(3):
            row = tk.Frame(right, bg="#1e1e1e")
            row.pack(fill="x", pady=2)
            lbl = tk.Label(row, text=f"—", bg="#1e1e1e", fg="white",
                           font=("Segoe UI", 14, "bold"), width=3)
            lbl.pack(side="left")
            bar_bg = tk.Frame(row, bg="#333", width=140, height=18)
            bar_bg.pack(side="left", padx=(6, 6))
            bar = tk.Frame(bar_bg, bg="#4CAF50", width=0, height=18)
            bar.place(x=0, y=0)
            pct = tk.Label(row, text="", bg="#1e1e1e", fg="#aaa", font=("Segoe UI", 10))
            pct.pack(side="left")
            self.pred_labels.append(lbl)
            self.pred_bars.append((bar_bg, bar, pct))

        self.result_label = tk.Label(right, text="Draw something!", bg="#1e1e1e",
                                     fg="#FFD54F", font=("Segoe UI", 12, "bold"), wraplength=220)
        self.result_label.pack(pady=(10, 0))

        # --- Controls ---
        controls = tk.Frame(main, bg="#1e1e1e")
        controls.grid(row=4, column=0, columnspan=2, pady=(14, 0), sticky="ew")

        tk.Button(controls, text="🤖 Guess", command=self.guess,
                  bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=18, pady=6).pack(side="left")
        tk.Button(controls, text="↩ Undo", command=self.undo,
                  bg="#444", fg="white", relief="flat", padx=12, pady=6).pack(side="left", padx=(8, 0))
        tk.Button(controls, text="🗑 Clear", command=self.clear,
                  bg="#444", fg="white", relief="flat", padx=12, pady=6).pack(side="left", padx=(8, 0))

        self.eraser_btn = tk.Button(controls, text="🧽 Eraser: OFF", command=self.toggle_eraser,
                                    bg="#444", fg="white", relief="flat", padx=12, pady=6)
        self.eraser_btn.pack(side="left", padx=(8, 0))

        tk.Label(controls, text="Brush:", bg="#1e1e1e", fg="white").pack(side="left", padx=(14, 4))
        ttk.Scale(controls, from_=4, to=28, variable=self.brush_size,
                  orient="horizontal", length=100).pack(side="left")

        # Keyboard
        root.bind("<Return>", lambda e: self.guess())
        root.bind("<Control-z>", lambda e: self.undo())
        root.bind("<Delete>", lambda e: self.clear())
        root.bind("c", lambda e: self.clear())

        self.update_preview()

    # --- Drawing ---
    def on_down(self, event: tk.Event) -> None:
        self.last_x, self.last_y = event.x, event.y
        self.current_stroke = [(event.x, event.y)]
        self._draw_dot(event.x, event.y)

    def on_drag(self, event: tk.Event) -> None:
        if self.last_x is None:
            return
        self._draw_line(self.last_x, self.last_y, event.x, event.y)
        self.last_x, self.last_y = event.x, event.y
        self.current_stroke.append((event.x, event.y))
        self.update_preview()  # live preview

    def on_up(self, event: tk.Event) -> None:
        if self.current_stroke:
            self.strokes.append(self.current_stroke)
            self.current_stroke = []
        self.last_x = self.last_y = None
        self.update_preview()

    def _draw_dot(self, x: int, y: int) -> None:
        r = self.brush_size.get() // 2
        col = "white" if self.eraser_on else "black"
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=col, outline=col)

    def _draw_line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        col = "white" if self.eraser_on else "black"
        w = self.brush_size.get()
        self.canvas.create_line(x1, y1, x2, y2, fill=col, width=w,
                                capstyle="round", joinstyle="round", smooth=True)
        # Round caps so lines don't look jagged
        self._draw_dot(x2, y2)

    def undo(self):
        if not self.strokes:
            return
        self.strokes.pop()
        self.redraw_all()
        self.update_preview()

    def clear(self):
        self.strokes = []
        self.canvas.delete("all")
        self.reset_predictions()
        self.result_label.config(text="Draw something!")
        self.update_preview()

    def redraw_all(self):
        self.canvas.delete("all")
        for stroke in self.strokes:
            for i in range(len(stroke)):
                x, y = stroke[i]
                self._draw_dot(x, y)
                if i > 0:
                    px, py = stroke[i - 1]
                    self._draw_line(px, py, x, y)

    def toggle_eraser(self):
        self.eraser_on = not self.eraser_on
        self.eraser_btn.config(
            text=f"🧽 Eraser: {'ON' if self.eraser_on else 'OFF'}",
            bg="#E74C3C" if self.eraser_on else "#444")

    # --- Prediction ---
    def get_pil_image(self):
        """Rebuild PIL image from canvas via strokes (more reliable than screenshot)."""
        img = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), color=255)
        d = ImageDraw.Draw(img)
        for stroke in self.strokes:
            for i, (x, y) in enumerate(stroke):
                r = self.brush_size.get() // 2
                d.ellipse([x - r, y - r, x + r, y + r], fill=0)
                if i > 0:
                    px, py = stroke[i - 1]
                    d.line([px, py, x, y], fill=0, width=self.brush_size.get())
        return img

    def update_preview(self):
        """Show 28x28 version the model sees, scaled up."""
        arr = preprocess_canvas(self.get_pil_image())
        # arr is white-on-black (0-1), preview wants same
        nearest = Image.Resampling.NEAREST if hasattr(Image, "Resampling") else Image.NEAREST
        img = Image.fromarray((arr * 255).astype(np.uint8)).resize((112, 112), resample=nearest)
        self.preview_img = ImageTk.PhotoImage(img)
        self.preview_label.config(image=self.preview_img)

    def guess(self):
        if not self.strokes:
            messagebox.showwarning("Empty", "Draw a digit first!")
            return
        arr = preprocess_canvas(self.get_pil_image())
        if arr.max() == 0:
            return

        probs = self.model.predict(arr.reshape(1, 28, 28), verbose=0)[0]
        top3 = np.argsort(probs)[::-1][:3]

        # Update bars
        for i, idx in enumerate(top3):
            pct = probs[idx] * 100
            lbl, (_, bar, pct_lbl) = self.pred_labels[i], self.pred_bars[i]
            lbl.config(text=str(idx))
            bar.config(width=int(140 * probs[idx]),
                       bg="#4CAF50" if i == 0 else "#777")
            pct_lbl.config(text=f"{pct:.1f}%")

        best = int(top3[0])
        conf = probs[top3[0]] * 100
        if conf > 90:
            msg = f"I'm {conf:.0f}% sure it's a {best}! 🎉"
        elif conf > 60:
            msg = f"Looks like a {best} ({conf:.0f}%)"
        else:
            msg = f"Hmm... maybe a {best}? Only {conf:.0f}% sure. Try drawing clearer."
        self.result_label.config(text=msg)

    def reset_predictions(self):
        for lbl, (bg, bar, pct_lbl) in zip(self.pred_labels, self.pred_bars):
            lbl.config(text="—")
            bar.config(width=0)
            pct_lbl.config(text="")

def main():
    if not HAS_TF:
        print("Install TensorFlow: pip install tensorflow pillow numpy")
        return

    root = tk.Tk()
    # Loading label while model loads
    loading = tk.Label(root, text="Loading / training model...\n(first run trains ~30s, then it saves)",
                       font=("Segoe UI", 12), padx=30, pady=30)
    loading.pack()
    root.update()

    model = get_model()
    loading.destroy()

    DrawingApp(root, model)
    root.mainloop()

if __name__ == "__main__":
    main()