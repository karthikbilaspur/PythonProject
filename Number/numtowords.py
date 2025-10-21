import num2words
import tkinter as tk
from tkinter import messagebox

class NumberToWordsConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Number to Words Converter")

        # Input frame
        self.input_frame = tk.Frame(self.window)
        self.input_frame.pack()

        self.label = tk.Label(self.input_frame, text="Enter a number:")
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.input_frame, width=20)
        self.entry.pack(side=tk.LEFT)

        # Language frame
        self.language_frame = tk.Frame(self.window)
        self.language_frame.pack()

        self.language_label = tk.Label(self.language_frame, text="Select language:")
        self.language_label.pack(side=tk.LEFT)

        self.language_var = tk.StringVar(self.language_frame)
        self.language_var.set("en")  # default value

        self.language_option = tk.OptionMenu(self.language_frame, self.language_var, "en", "es", "fr", "de", "it")
        self.language_option.pack(side=tk.LEFT)

        # Conversion type frame
        self.conversion_type_frame = tk.Frame(self.window)
        self.conversion_type_frame.pack()

        self.conversion_type_var = tk.StringVar(self.conversion_type_frame)
        self.conversion_type_var.set("cardinal")  # default value

        self.conversion_type_menu = tk.OptionMenu(self.conversion_type_frame, self.conversion_type_var, "cardinal", "ordinal", "currency")
        self.conversion_type_menu.pack(side=tk.LEFT)

        # Button frame
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack()

        self.convert_button = tk.Button(self.button_frame, text="Convert", command=self.convert_number)
        self.convert_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT)

        # Result frame
        self.result_frame = tk.Frame(self.window)
        self.result_frame.pack()

        self.result_label = tk.Label(self.result_frame, text="")
        self.result_label.pack()

    def convert_number(self):
        try:
            num = int(self.entry.get())
            language = self.language_var.get()
            conversion_type = self.conversion_type_var.get()

            if conversion_type == "cardinal":
                words = num2words.num2words(num, lang=language)
            elif conversion_type == "ordinal":
                words = num2words.num2words(num, lang=language, to="ordinal")
            elif conversion_type == "currency":
                words = num2words.num2words(num, lang=language, to="currency")

            self.result_label['text'] = words
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a number.")

    def clear_fields(self):
        self.entry.delete(0, tk.END)
        self.result_label['text'] = ""

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    converter = NumberToWordsConverter()
    converter.run()