import os
import tkinter as tk
from tkinter import filedialog

class DiskSpaceAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Disk Space Analyzer")
        self.path_label = tk.Label(self.root, text="Select path to analyze:")
        self.path_label.pack()
        self.path_entry = tk.Entry(self.root, width=50)
        self.path_entry.pack()
        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_path)
        self.browse_button.pack()
        self.analyze_button = tk.Button(self.root, text="Analyze", command=self.analyze_disk_space)
        self.analyze_button.pack()
        self.result_text = tk.Text(self.root, height=20, width=60)
        self.result_text.pack()

    def browse_path(self):
        path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def get_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def analyze_disk_space(self):
        path = self.path_entry.get()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Analyzing disk space for {path}...\n")
        total_size = self.get_size(path)
        self.result_text.insert(tk.END, f"Total size: {total_size / (1024 * 1024):.2f} MB\n")

        # Get top 10 largest files
        largest_files = []
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                size = os.path.getsize(fp)
                largest_files.append((fp, size))
        largest_files.sort(key=lambda x: x[1], reverse=True)
        self.result_text.insert(tk.END, "Top 10 largest files:\n")
        for file, size in largest_files[:10]:
            self.result_text.insert(tk.END, f"{file}: {size / (1024 * 1024):.2f} MB\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    analyzer = DiskSpaceAnalyzer()
    analyzer.run()