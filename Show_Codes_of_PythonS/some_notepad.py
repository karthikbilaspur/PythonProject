import tkinter as tk
from tkinter import filedialog, messagebox
import os

class Notepad:
    def __init__(self, **kwargs: dict[str, int]) -> None:
        self.__root = tk.Tk()
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisWidth = kwargs.get('width', 300)
        self.__thisHeight = kwargs.get('height', 300)

        self.__create_widgets()
        self.__configure_window()
        self.__create_menu_items()

    def __create_widgets(self):
        self.__thisTextArea = tk.Text(self.__root)
        self.__thisScrollBar = tk.Scrollbar(self.__thisTextArea)
        self.__thisMenuBar = tk.Menu(self.__root)
        self.__thisFileMenu = tk.Menu(self.__thisMenuBar, tearoff=0)
        self.__thisEditMenu = tk.Menu(self.__thisMenuBar, tearoff=0)
        self.__thisHelpMenu = tk.Menu(self.__thisMenuBar, tearoff=0)

    def __configure_window(self):
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except tk.TCL_ERROR:
            pass

        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        left = (screen_width / 2) - (self.__thisWidth / 2)
        top = (screen_height / 2) - (self.__thisHeight / 2)
        self.__root.geometry(f'{self.__thisWidth}x{self.__thisHeight}+{int(left)}+{int(top)}')

        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__thisTextArea.grid(sticky="nsew")
        self.__thisScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __create_menu_items(self):
        self.__thisFileMenu.add_command(label="New", command=self.__new_file)
        self.__thisFileMenu.add_command(label="Open", command=self.__open_file)
        self.__thisFileMenu.add_command(label="Save", command=self.__save_file)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quit_application)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        self.__thisHelpMenu.add_command(label="About Notepad", command=self.__show_about)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

    def __quit_application(self):
        self.__root.destroy()

    def __show_about(self):
        messagebox.showinfo("Notepad", "Mrinal Verma")

    def __open_file(self):
        self.__file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete('1.0', tk.END)
            with open(self.__file, "r") as file:
                self.__thisTextArea.insert('1.0', file.read())

    def __new_file(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete('1.0', tk.END)

    def __save_file(self):
        if not self.__file:
            self.__file = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file:
            with open(self.__file, "w") as file:
                file.write(self.__thisTextArea.get('1.0', tk.END))
            self.__root.title(os.path.basename(self.__file) + " - Notepad")

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        self.__root.mainloop()

if __name__ == "__main__":
    notepad = Notepad(width=600, height=400)
    notepad.run()