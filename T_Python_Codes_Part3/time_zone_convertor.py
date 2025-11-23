import tkinter as tk
from tkinter import ttk
import pytz
from datetime import datetime

class TimezoneConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Timezone Converter")

        # Create input frame
        self.input_frame = tk.Frame(self.window)
        self.input_frame.pack(padx=10, pady=10)

        # Create timezone labels and comboboxes
        self.from_label = tk.Label(self.input_frame, text="From:")
        self.from_label.grid(row=0, column=0, padx=5, pady=5)
        self.from_timezone = tk.StringVar()
        self.from_timezone.set("US/Pacific")
        self.from_combobox = ttk.Combobox(self.input_frame, textvariable=self.from_timezone)
        self.from_combobox['values'] = tuple(pytz.common_timezones)
        self.from_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.to_label = tk.Label(self.input_frame, text="To:")
        self.to_label.grid(row=1, column=0, padx=5, pady=5)
        self.to_timezone = tk.StringVar()
        self.to_timezone.set("US/Eastern")
        self.to_combobox = ttk.Combobox(self.input_frame, textvariable=self.to_timezone)
        self.to_combobox['values'] = tuple(pytz.common_timezones)
        self.to_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Create datetime label and entry
        self.datetime_label = tk.Label(self.input_frame, text="Date and Time (YYYY-MM-DD HH:MM:SS):")
        self.datetime_label.grid(row=2, column=0, padx=5, pady=5)
        self.datetime_entry = tk.Entry(self.input_frame)
        self.datetime_entry.grid(row=2, column=1, padx=5, pady=5)

        # Create convert button
        self.convert_button = tk.Button(self.input_frame, text="Convert", command=self.convert_time)
        self.convert_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Create result label
        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack(padx=10, pady=10)

    def convert_time(self):
        try:
            from_tz = pytz.timezone(self.from_timezone.get())
            to_tz = pytz.timezone(self.to_timezone.get())
            datetime_str = self.datetime_entry.get()
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            from_time = from_tz.localize(datetime_obj)
            to_time = from_time.astimezone(to_tz)
            result = f"{datetime_str} {self.from_timezone.get()} is {to_time.strftime('%Y-%m-%d %H:%M:%S')} {self.to_timezone.get()}"
            self.result_label.config(text=result)
        except Exception as e:
            self.result_label.config(text="Invalid input")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    converter = TimezoneConverter()
    converter.run()