import tkinter as tk

class DistanceConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Distance Converter")

        # Input frame
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()
        self.distance_label = tk.Label(self.input_frame, text="Distance:")
        self.distance_label.pack(side=tk.LEFT)
        self.distance_entry = tk.Entry(self.input_frame, width=20)
        self.distance_entry.pack(side=tk.LEFT)

        # Unit selection frame
        self.unit_frame = tk.Frame(self.root)
        self.unit_frame.pack()
        self.from_unit_label = tk.Label(self.unit_frame, text="From:")
        self.from_unit_label.pack(side=tk.LEFT)
        self.from_unit = tk.StringVar()
        self.from_unit.set("Kilometers")
        self.from_unit_option = tk.OptionMenu(self.unit_frame, self.from_unit, "Kilometers", "Miles", "Meters", "Yards", "Feet")
        self.from_unit_option.pack(side=tk.LEFT)
        self.to_unit_label = tk.Label(self.unit_frame, text="To:")
        self.to_unit_label.pack(side=tk.LEFT)
        self.to_unit = tk.StringVar()
        self.to_unit.set("Miles")
        self.to_unit_option = tk.OptionMenu(self.unit_frame, self.to_unit, "Kilometers", "Miles", "Meters", "Yards", "Feet")
        self.to_unit_option.pack(side=tk.LEFT)

        # Convert button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_distance)
        self.convert_button.pack()

        # Result label
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def convert_distance(self):
        try:
            distance = float(self.distance_entry.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()

            # Conversion factors
            conversion_factors = {
                "Kilometers": {"Kilometers": 1, "Miles": 0.621371, "Meters": 1000, "Yards": 1093.61, "Feet": 3280.84},
                "Miles": {"Kilometers": 1.60934, "Miles": 1, "Meters": 1609.34, "Yards": 1760, "Feet": 5280},
                "Meters": {"Kilometers": 0.001, "Miles": 0.000621371, "Meters": 1, "Yards": 1.09361, "Feet": 3.28084},
                "Yards": {"Kilometers": 0.0009144, "Miles": 0.000568182, "Meters": 0.9144, "Yards": 1, "Feet": 3},
                "Feet": {"Kilometers": 0.0003048, "Miles": 0.000189394, "Meters": 0.3048, "Yards": 0.333333, "Feet": 1}
            }

            result = distance * conversion_factors[from_unit][to_unit]
            self.result_label.config(text=f"{distance} {from_unit} is equal to {result:.4f} {to_unit}")
        except ValueError:
            self.result_label.config(text="Invalid input")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    converter = DistanceConverter()
    converter.run()