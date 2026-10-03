import cv2
import numpy as np
from sklearn.cluster import KMeans
import tkinter as tk
from tkinter import filedialog, messagebox

def detect_colors(image_path, n_colors=5):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    # Resize for speed - massive speedup
    image = cv2.resize(image, (300, 300), interpolation=cv2.INTER_AREA)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape to (pixels, 3)
    data = image.reshape((-1, 3))

    # K-means
    kmeans = KMeans(n_clusters=n_colors, n_init=10, random_state=42)
    kmeans.fit(data)

    # Count labels to get percentage
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    total = counts.sum()

    # Sort by dominance (most frequent first)
    sorted_idx = np.argsort(counts)[::-1]

    result = []
    for idx in sorted_idx:
        color = kmeans.cluster_centers_[idx]
        count = counts[idx]
        percent = (count / total) * 100
        rgb = tuple(map(int, color))
        hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)
        result.append({
            "rgb": rgb,
            "hex": hex_color,
            "percent": percent
        })

    return result

# ---------- GUI ----------

def select_image():
    path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
    )
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def detect_colors_gui():
    image_path = entry.get()
    if not image_path:
        messagebox.showwarning("Warning", "Select an image first")
        return

    try:
        colors = detect_colors(image_path, n_colors=int(cluster_var.get()))

        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f"Dominant colors from {image_path.split('/')[-1]}:\n\n")
        for i, c in enumerate(colors):
            result_text.insert(tk.END, f"{i+1}. {c['hex']} RGB{c['rgb']} - {c['percent']:.1f}%\n")

        # Draw swatches
        canvas.delete("all")
        swatch_width = 400 // len(colors)
        for i, c in enumerate(colors):
            x0 = i * swatch_width
            x1 = (i+1) * swatch_width
            canvas.create_rectangle(x0, 0, x1, 80, fill=c['hex'], outline="")
            canvas.create_text(x0 + swatch_width//2, 95, text=f"{c['percent']:.0f}%", font=("Arial", 10, "bold"))

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Build GUI
root = tk.Tk()
root.title("Dominant Color Detector")
root.geometry("500x400")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill='x')

tk.Label(frame, text="Image:").pack(side=tk.LEFT)
entry = tk.Entry(frame, width=40)
entry.pack(side=tk.LEFT, padx=5, fill='x', expand=True)
tk.Button(frame, text="Browse", command=select_image).pack(side=tk.LEFT)

opt_frame = tk.Frame(root)
opt_frame.pack(pady=5)
tk.Label(opt_frame, text="Number of colors:").pack(side=tk.LEFT)
cluster_var = tk.StringVar(value="5")
tk.Spinbox(opt_frame, from_=2, to=10, textvariable=cluster_var, width=5).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="Detect Colors", command=detect_colors_gui, bg="#4CAF50", fg="white", height=2).pack(pady=10, fill='x', padx=20)

canvas = tk.Canvas(root, height=110, bg="white")
canvas.pack(fill='x', padx=10)

result_text = tk.Text(root, height=8)
result_text.pack(padx=10, pady=10, fill='both', expand=True)

# CLI mode still works
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # python main.py image.jpg
        colors = detect_colors(sys.argv[1])
        print("Dominant colors:")
        for c in colors:
            print(f"{c['hex']} - {c['percent']:.1f}% RGB{c['rgb']}")
    else:
        root.mainloop()