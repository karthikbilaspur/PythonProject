import tkinter as tk
from tkinter import messagebox
import random
import time

class LinearSearchVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Linear Search Visualizer")
        self.root.config(bg="#f0f0f0")
        self.array = []
        self.canvas = tk.Canvas(self.root, width=1000, height=380, bg="#C3FDB8")
        self.canvas.pack()
        self.entries_frame = tk.Frame(self.root, bg="#98AFC7")
        self.entries_frame.pack()
        self.create_widgets()

    def create_widgets(self):
        # Size of array entry
        tk.Label(self.entries_frame, text="Size of array:", bg="#C3FDB8").grid(row=0, column=0)
        self.size_entry = tk.Entry(self.entries_frame)
        self.size_entry.grid(row=0, column=1)

        # Minimum element entry
        tk.Label(self.entries_frame, text="Minimum element:", bg="#C3FDB8").grid(row=0, column=2)
        self.min_entry = tk.Entry(self.entries_frame)
        self.min_entry.grid(row=0, column=3)

        # Maximum element entry
        tk.Label(self.entries_frame, text="Maximum element:", bg="#C3FDB8").grid(row=0, column=4)
        self.max_entry = tk.Entry(self.entries_frame)
        self.max_entry.grid(row=0, column=5)

        # Generate button
        tk.Button(self.entries_frame, text="Generate", command=self.generate_array).grid(row=1, column=0, columnspan=2)

        # Key to search entry
        tk.Label(self.entries_frame, text="Key:", bg="#C3FDB8").grid(row=1, column=2)
        self.key_entry = tk.Entry(self.entries_frame)
        self.key_entry.grid(row=1, column=3)

        # Search button
        tk.Button(self.entries_frame, text="Search", command=self.search).grid(row=1, column=4, columnspan=2)

    def generate_array(self):
        try:
            size = int(self.size_entry.get())
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
            self.array = [random.randint(min_val, max_val) for _ in range(size)]
            self.draw_rectangles(self.array, ["#98AFC7"] * len(self.array))
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def search(self):
        try:
            key = int(self.key_entry.get())
            self.linear_search(key)
        except ValueError:
            messagebox.showerror("Error", "Invalid key")

    def linear_search(self, key):
        colors = ["#98AFC7"] * len(self.array)
        for i in range(len(self.array)):
            colors[i] = "white"
            self.draw_rectangles(self.array, colors)
            self.root.update_idletasks()
            time.sleep(0.2)
            if self.array[i] == key:
                colors[i] = "green"
                self.draw_rectangles(self.array, colors)
                messagebox.showinfo("Result", "Key found")
                return
            else:
                colors[i] = "#98AFC7"
                self.draw_rectangles(self.array, colors)
                self.root.update_idletasks()
                time.sleep(0.2)
        messagebox.showinfo("Result", "Key not found")

    def draw_rectangles(self, array, colors):
        self.canvas.delete("all")
        canvas_width = 1000
        canvas_height = 380
        bar_width = canvas_width / len(array)
        offset = 4
        for i, height in enumerate(array):
            x0 = i * bar_width
            y0 = canvas_height - height / max(array) * (canvas_height - offset)
            x1 = (i + 1) * bar_width
            y1 = canvas_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i])
            self.canvas.create_text(x0 + bar_width / 2, y0, text=str(height))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    visualizer = LinearSearchVisualizer()
    visualizer.run()