import cv2
import numpy as np
from sklearn.cluster import KMeans
import tkinter as tk
from tkinter import filedialog

def detect_colors(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a feature vector
    image = image.reshape((-1, 3))

    # Perform K-means clustering to detect dominant colors
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(image)

    # Get the dominant colors
    colors = kmeans.cluster_centers_

    # Convert the colors to hexadecimal format
    hex_colors = []
    for color in colors:
        hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))
        hex_colors.append(hex_color)

    return hex_colors

def select_image():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
    if image_path:
        entry.delete(0, tk.END)
        entry.insert(0, image_path)

def detect_colors_gui():
    image_path = entry.get()
    if image_path:
        colors = detect_colors(image_path)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Dominant colors:\n")
        for i, color in enumerate(colors):
            result_text.insert(tk.END, f"Color {i+1}: {color}\n")

root = tk.Tk()
root.title("Color Detection")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Image Path:")
label.pack(side=tk.LEFT)

entry = tk.Entry(frame, width=50)
entry.pack(side=tk.LEFT)

button = tk.Button(frame, text="Browse", command=select_image)
button.pack(side=tk.LEFT)

detect_button = tk.Button(root, text="Detect Colors", command=detect_colors_gui)
detect_button.pack(pady=10)

result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()