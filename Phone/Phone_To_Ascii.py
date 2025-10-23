import tkinter as tk
from tkinter import messagebox
import pyfiglet

class PhoneToASCII:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Phone to ASCII Art")

        # Create input field for phone number
        self.phone_number_label = tk.Label(self.window, text="Enter Phone Number:")
        self.phone_number_label.pack()
        self.phone_number_entry = tk.Entry(self.window)
        self.phone_number_entry.pack()

        # Create font style options
        self.font_styles = ["standard", "slant", "script", "digital", "bubble"]
        self.font_style_var = tk.StringVar(self.window)
        self.font_style_var.set(self.font_styles[0])
        self.font_style_option = tk.OptionMenu(self.window, self.font_style_var, *self.font_styles)
        self.font_style_option.pack()

        # Create button to convert phone number to ASCII
        self.convert_button = tk.Button(self.window, text="Convert to ASCII", command=self.convert_to_ascii)
        self.convert_button.pack()

        # Create text area to display result
        self.result_text = tk.Text(self.window, height=20, width=60)
        self.result_text.pack()

    def convert_to_ascii(self):
        phone_number = self.phone_number_entry.get()
        font_style = self.font_style_var.get()

        try:
            ascii_art = pyfiglet.figlet_format(phone_number, font=font_style)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, ascii_art)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    converter = PhoneToASCII()
    converter.run()