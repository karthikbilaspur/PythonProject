import tkinter as tk
from math import sqrt

class DistanceCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Distance Calculator")

        # Input frame
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()
        self.point1_label = tk.Label(self.input_frame, text="Point 1 (x, y):")
        self.point1_label.pack(side=tk.LEFT)
        self.x1_entry = tk.Entry(self.input_frame, width=5)
        self.x1_entry.pack(side=tk.LEFT)
        self.y1_entry = tk.Entry(self.input_frame, width=5)
        self.y1_entry.pack(side=tk.LEFT)

        self.point2_label = tk.Label(self.input_frame, text="Point 2 (x, y):")
        self.point2_label.pack(side=tk.LEFT)
        self.x2_entry = tk.Entry(self.input_frame, width=5)
        self.x2_entry.pack(side=tk.LEFT)
        self.y2_entry = tk.Entry(self.input_frame, width=5)
        self.y2_entry.pack(side=tk.LEFT)

        # Calculate button
        self.calculate_button = tk.Button(self.root, text="Calculate Distance", command=self.calculate_distance)
        self.calculate_button.pack()

        # Result frame
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack()
        self.distance_label = tk.Label(self.result_frame, text="Distance:")
        self.distance_label.pack(side=tk.LEFT)
        self.distance_result = tk.Label(self.result_frame, text="")
        self.distance_result.pack(side=tk.LEFT)

        self.midpoint_label = tk.Label(self.result_frame, text="Midpoint:")
        self.midpoint_label.pack(side=tk.LEFT)
        self.midpoint_result = tk.Label(self.result_frame, text="")
        self.midpoint_result.pack(side=tk.LEFT)

        # Clear button
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_fields)
        self.clear_button.pack()

    def calculate_distance(self):
        try:
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
            x2 = float(self.x2_entry.get())
            y2 = float(self.y2_entry.get())

            distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
            self.distance_result.config(text=f"{distance:.4f} units")

            midpoint_x = (x1 + x2) / 2
            midpoint_y = (y1 + y2) / 2
            self.midpoint_result.config(text=f"({midpoint_x:.2f}, {midpoint_y:.2f})")
        except ValueError:
            self.distance_result.config(text="Invalid input")
            self.midpoint_result.config(text="")

    def clear_fields(self):
        self.x1_entry.delete(0, tk.END)
        self.y1_entry.delete(0, tk.END)
        self.x2_entry.delete(0, tk.END)
        self.y2_entry.delete(0, tk.END)
        self.distance_result.config(text="")
        self.midpoint_result.config(text="")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    calculator = DistanceCalculator()
    calculator.run()