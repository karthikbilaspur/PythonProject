import tkinter as tk
from tkinter import messagebox

class CustomGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom GUI")

        # Label
        self.label = tk.Label(root, text="Welcome to Custom GUI")
        self.label.pack()

        # Button
        self.button = tk.Button(root, text="Click Me", command=self.button_click)
        self.button.pack()

        # Entry
        self.entry_label = tk.Label(root, text="Enter your name:")
        self.entry_label.pack()
        self.entry = tk.Entry(root)
        self.entry.pack()

        # Text Box
        self.text_box_label = tk.Label(root, text="Enter your message:")
        self.text_box_label.pack()
        self.text_box = tk.Text(root, height=5, width=30)
        self.text_box.pack()

        # Checkbutton
        self.check_var = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(root, text="Check me", variable=self.check_var)
        self.checkbutton.pack()

        # Radiobuttons
        self.radio_var = tk.StringVar()
        self.radiobutton1 = tk.Radiobutton(root, text="Option 1", variable=self.radio_var, value="Option 1")
        self.radiobutton1.pack()
        self.radiobutton2 = tk.Radiobutton(root, text="Option 2", variable=self.radio_var, value="Option 2")
        self.radiobutton2.pack()

        # Dropdown
        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Select an option")
        self.dropdown = tk.OptionMenu(root, self.dropdown_var, "Option 1", "Option 2", "Option 3")
        self.dropdown.pack()

    def button_click(self):
        name = self.entry.get()
        message = self.text_box.get("1.0", tk.END)
        check_status = self.check_var.get()
        radio_status = self.radio_var.get()
        dropdown_status = self.dropdown_var.get()

        messagebox.showinfo("Info", f"Name: {name}\nMessage: {message}\nCheck Status: {check_status}\nRadio Status: {radio_status}\nDropdown Status: {dropdown_status}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomGUI(root)
    root.mainloop()