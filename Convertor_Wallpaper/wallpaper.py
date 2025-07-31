from tkinter import *
from tkinter import filedialog
from wallpaper import set_wallpaper

def change_wallpaper():
    try:
        set_wallpaper(str(path.get()))
        status.set("Wallpaper changed successfully!")
    except Exception as e:
        status.set(f"Error: {str(e)}")

def browse_files():
    filename = filedialog.askopenfilename(initialdir="/", 
                                          title="Select a File", 
                                          filetypes=(("Image files", ".jpg .jpeg .png"), ("All files", "*.*")))
    path.set(filename)
    file_label.config(text=f"File Opened: {filename}")

root = Tk()
root.configure(bg='light grey')

path = StringVar()
status = StringVar()

file_label = Label(root, text="Select an image", width=100, fg="blue")
file_label.grid(column=1, row=1)

Label(root, text="Select image:", bg="light grey").grid(row=0, sticky=W)
Label(root, text="Status:", bg="light grey").grid(row=3, sticky=W)
Label(root, textvariable=status, bg="light grey").grid(row=3, column=1, sticky=W)

open_button = Button(root, text="Open", command=browse_files, bg="white")
open_button.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=5)

apply_button = Button(root, text="Apply", command=change_wallpaper, bg="white")
apply_button.grid(row=2, column=2, columnspan=2, rowspan=2, padx=5, pady=5)

root.mainloop()