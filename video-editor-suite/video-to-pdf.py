import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import VideoFileClip
from PIL import Image
import os
class VideoToPdf:
    def __init__(self, parent: tk.Misc | None = None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Video to PDF")
        self.window.geometry("450x240")
        tk.Label(self.window, text="Select a video file:", font=("Arial", 11, "bold")).pack(pady=10)
        self.file_entry = tk.Entry(self.window, width=55); self.file_entry.pack(padx=10)
        tk.Button(self.window, text="Browse", command=self.browse_file).pack(pady=5)
        tk.Label(self.window, text="Frames per second to extract:").pack(pady=5)
        self.fps_var = tk.StringVar(value="1")
        tk.Entry(self.window, textvariable=self.fps_var, width=10).pack()
        tk.Button(self.window, text="Convert to PDF", bg="#FF9800", fg="white", command=self.convert_to_pdf).pack(pady=10)
        self.save_label = tk.Label(self.window, text="", wraplength=400, fg="green"); self.save_label.pack()
    def browse_file(self):
        p = filedialog.askopenfilename(filetypes=[("Video Files","*.mp4 *.avi *.mov *.mkv")])
        if p: self.file_entry.delete(0, tk.END); self.file_entry.insert(0, p)
    def convert_to_pdf(self):
        fp = self.file_entry.get().strip()
        if not fp: messagebox.showwarning("Missing","Please select a video file"); return
        try:
            fps = float(self.fps_var.get() or 1)
            self.save_label.config(text="Extracting..."); self.window.update()
            video = VideoFileClip(fp)
            frames = [Image.fromarray(f) for f in video.iter_frames(fps=fps, dtype="uint8")]
            video.close()
            if not frames: raise ValueError("No frames extracted")
            save = os.path.splitext(fp)[0] + ".pdf"
            frames[0].save(save, save_all=True, append_images=frames[1:])
            self.save_label.config(text=f"PDF saved: {save} ({len(frames)} pages)")
        except Exception as e: messagebox.showerror("Error", str(e))
    def run(self): self.window.mainloop()
def open_window(parent: tk.Misc | None = None) -> VideoToPdf: return VideoToPdf(parent)
if __name__ == "__main__": VideoToPdf().run()
