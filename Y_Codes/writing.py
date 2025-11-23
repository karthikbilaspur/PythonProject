import tkinter as tk
from tkinter import filedialog, messagebox

class YouTubeScriptWriter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Script Writer")

        # Create frames
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)

        # Create labels and entries
        self.title_label = tk.Label(self.frame1, text="Title:")
        self and.title_entry = tk.Entry(self.frame1)
        self.description_label = tk.Label(self.frame2, text="Description:")
        self.description_text = tk.Text(self.frame2, height=10, width=50)
        self.script_label = tk.Label(self.frame3, text="Script:")
        self.script_text = tk.Text(self.frame3, height=20, width=50)

        # Create buttons
        self.save_button = tk.Button(self.frame3, text="Save", command=self.save_script)
        self.clear_button = tk.Button(self.frame3, text="Clear", command=self.clear_script)

        # Layout frames and widgets
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.title_label.pack(side=tk.LEFT)
        self.title_entry.pack(side=tk.LEFT)
        self.description_label.pack(side=tk.TOP)
        self.description_text.pack(side=tk.TOP)
        self.script_label.pack(side=tk.TOP)
        self.script_text.pack(side=tk.TOP)
        self.save_button.pack(side=tk.LEFT)
        self.clear_button.pack(side=tk.LEFT)

    def save_script(self):
        title = self.title_entry.get()
        description = self.description_text.get("1.0", tk.END)
        script = self.script_text.get("1.0", tk.END)
        file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_name:
            with open(file_name, "w") as file:
                file.write("Title: " + title + "\n\n")
                file.write("Description: " + description + "\n\n")
                file.write("Script: " + script)
            messagebox.showinfo("Script Saved", "Script saved successfully.")

    def clear_script(self):
        self.title_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
        self.script_text.delete("1.0", tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    writer = YouTubeScriptWriter()
    writer.run()self.title_entry = tk.Entry(self.frame1)