import tkinter as tk
from tkinter import ttk
from pint import UnitRegistry

ureg = UnitRegistry()

class TemperatureConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Converter")

        # Create tabs
        self.tab_control = ttk.Notebook(self.root)
        self.celsius_tab = ttk.Frame(self.tab_control)
        self.fahrenheit_tab = ttk.Frame(self.tab_control)
        self.kelvin_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.celsius_tab, text="Celsius")
        self.tab_control.add(self.fahrenheit_tab, text="Fahrenheit")
        self.tab_control.add(self.kelvin_tab, text="Kelvin")
        self.tab_control.pack(expand=1, fill="both")

        # Celsius tab
        self.celsius_label = tk.Label(self.celsius_tab, text="Celsius:")
        self.celsius_label.pack()
        self.celsius_entry = tk.Entry(self.celsius_tab)
        self.celsius_entry.pack()
        self.celsius_to_fahrenheit_button = tk.Button(self.celsius_tab, text="Convert to Fahrenheit", command=self.celsius_to_fahrenheit)
        self.celsius_to_fahrenheit_button.pack()
        self.celsius_to_kelvin_button = tk.Button(self.celsius_tab, text="Convert to Kelvin", command=self.celsius_to_kelvin)
        self.celsius_to_kelvin_button.pack()
        self.celsius_result_label = tk.Label(self.celsius_tab, text="")
        self.celsius_result_label.pack()

        # Fahrenheit tab
        self.fahrenheit_label = tk.Label(self.fahrenheit_tab, text="Fahrenheit:")
        self.fahrenheit_label.pack()
        self.fahrenheit_entry = tk.Entry(self.fahrenheit_tab)
        self.fahrenheit_entry.pack()
        self.fahrenheit_to_celsius_button = tk.Button(self.fahrenheit_tab, text="Convert to Celsius", command=self.fahrenheit_to_celsius)
        self.fahrenheit_to_celsius_button.pack()
        self.fahrenheit_to_kelvin_button = tk.Button(self.fahrenheit_tab, text="Convert to Kelvin", command=self.fahrenheit_to_kelvin)
        self.fahrenheit_to_kelvin_button.pack()
        self.fahrenheit_result_label = tk.Label(self.fahrenheit_tab, text="")
        self.fahrenheit_result_label.pack()

        # Kelvin tab
        self.kelvin_label = tk.Label(self.kelvin_tab, text="Kelvin:")
        self.kelvin_label.pack()
        self.kelvin_entry = tk.Entry(self.kelvin_tab)
        self.kelvin_entry.pack()
        self.kelvin_to_celsius_button = tk.Button(self.kelvin_tab, text="Convert to Celsius", command=self.kelvin_to_celsius)
        self.kelvin_to_celsius_button.pack()
        self.kelvin_to_fahrenheit_button = tk.Button(self.kelvin_tab, text="Convert to Fahrenheit", command=self.kelvin_to_fahrenheit)
        self.kelvin_to_fahrenheit_button.pack()
        self.kelvin_result_label = tk.Label(self.kelvin_tab, text="")
        self.kelvin_result_label.pack()

    def celsius_to_fahrenheit(self):
        try:
            celsius = float(self.celsius_entry.get())
            fahrenheit = (celsius * ureg.degC).to(ureg.degF).magnitude
            self.celsius_result_label.config(text=f"{celsius}°C is equal to {fahrenheit}°F")
        except ValueError:
            self.celsius_result_label.config(text="Invalid input")

    def celsius_to_kelvin(self):
        try:
            celsius = float(self.celsius_entry.get())
            kelvin = (celsius * ureg.degC).to(ureg.kelvin).magnitude
            self.celsius_result_label.config(text=f"{celsius}°C is equal to {kelvin}K")
        except ValueError:
            self.celsius_result_label.config(text="Invalid input")

    def fahrenheit_to_celsius(self):
        try:
            fahrenheit = float(self.fahrenheit_entry.get())
            celsius = (fahrenheit * ureg.degF).to(ureg.degC).magnitude
            self.fahrenheit_result_label.config(text=f"{fahrenheit}°F is equal to {celsius}°C")
        except ValueError:
            self.fahrenheit_result_label.config(text="Invalid input")

    def fahrenheit_to_kelvin(self):
        try:
            fahrenheit = float(self.fahrenheit_entry.get())
            kelvin = (fahrenheit * ureg.degF).to(ureg.kelvin).magnitude
            self.fahrenheit_result_label.config(text=f"{fahrenheit}°F is equal to {kelvin}K")
        except ValueError:
            self.fahrenheit_result_label.config(text="Invalid input")

    def kelvin_to_celsius(self):
        try:
            kelvin = float(self.kelvin_entry.get())
            celsius = (kelvin * ureg.kelvin).to(ureg.degC).magnitude
            self.kelvin_result_label.config(text=f"{kelvin}K is equal to {celsius}°C")
        except ValueError:
            self.kelvin_result_label.config(text="Invalid input")

    def kelvin_to_fahrenheit(self):
        try:
            kelvin = float(self.kelvin_entry.get())
            fahrenheit = (kelvin * ureg.kelvin).to(ureg.degF).magnitude
            self.kelvin_result_label.config(text=f"{kelvin}K is equal to {fahrenheit}°F")
        except ValueError:
            self.kelvin_result_label.config(text="Invalid input")

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureConverter(root)
    root.mainloop()