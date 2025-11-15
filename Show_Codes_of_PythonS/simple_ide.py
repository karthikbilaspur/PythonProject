import tkinter as tk
from tkinter import filedialog, messagebox

class IDE:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Programming Languages IDE")
        self.file_path = None

        self.text_area = tk.Text(self.root)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run Python", command=self.run_python)
        self.run_menu.add_command(label="Run Java", command=self.run_java)
        self.run_menu.add_command(label="Run C++", command=self.run_cpp)

        self.output_area = tk.Text(self.root, height=10)
        self.output_area.pack(fill=tk.BOTH)

    def new_file(self):
        self.text_area.delete('1.0', tk.END)
        self.file_path = None

    def open_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            with open(self.file_path, 'r') as file:
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert('1.0', file.read())

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename()
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.text_area.get('1.0', tk.END))

    def run_python(self):
        try:
            code = self.text_area.get('1.0', tk.END)
            output = exec(code)
            self.output_area.delete('1.0', tk.END)
            self.output_area.insert('1.0', str(output))
        except Exception as e:
            self.output_area.delete('1.0', tk.END)
            self.output_area.insert('1.0', str(e))

    def run_java(self):
        # Java compilation and execution is complex and requires external tools
        # This is a simplified example and may not work for all cases
        import os
        self.save_file()
        if self.file_path:
            class_name = os.path.basename(self.file_path).split('.')[0]
            os.system(f'javac {self.file_path}')
            output = os.popen(f'java {class_name}').read()
            self.output_area.delete('1.0', tk.END)
            self.output_area.insert('1.0', output)

    def run_cpp(self):
        # C++ compilation and execution is complex and requires external tools
        # This is a simplified example and may not work for all cases
        import os
        self.save_file()
        if self.file_path:
            output_file = self.file_path.split('.')[0]
            os.system(f'g++ {self.file_path} -o {output_file}')
            output = os.popen(f'{output_file}').read()
            self.output_area.delete('1.0', tk.END)
            self.output_area.insert('1.0', output)

if __name__ == "__main__":
    root = tk.Tk()
    ide = IDE(root)
    root.mainloop()