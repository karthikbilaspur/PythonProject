import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os

def add_watermark(video_file: str, watermark_file: str, output_file: str, opacity: float = 0.5) -> str:
    video = cv2.VideoCapture(video_file)
    if not video.isOpened():
        raise ValueError("Cannot open video file")
    watermark = cv2.imread(watermark_file, cv2.IMREAD_UNCHANGED)
    if watermark is None:
        raise ValueError("Cannot read watermark image")
    fps = video.get(cv2.CAP_PROP_FPS) or 30
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # Resize watermark if bigger than video
    max_w, max_h = width // 4, height // 4
    h, w = watermark.shape[:2]
    if w > max_w or h > max_h:
        scale = min(max_w / w, max_h / h)
        watermark = cv2.resize(watermark, (int(w*scale), int(h*scale)))
    fourcc = int.from_bytes(b"mp4v", byteorder="little")
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    while True:
        ret, frame = video.read()
        if not ret:
            break
        h, w = watermark.shape[:2]
        x, y = width - w - 10, height - h - 10
        roi = frame[y:y+h, x:x+w]
        # Handle alpha channel if present
        if watermark.shape[2] == 4:
            wm_bgr = watermark[:, :, :3]
            alpha = watermark[:, :, 3:4] / 255.0 * opacity
            frame[y:y+h, x:x+w] = (roi * (1-alpha) + wm_bgr * alpha).astype("uint8")
        else:
            frame[y:y+h, x:x+w] = cv2.addWeighted(roi, 1, watermark, opacity, 0)
        out.write(frame)
    video.release(); out.release()
    return output_file

class WatermarkTool:
    def __init__(self, parent: tk.Misc | None = None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Add Watermark to Video")
        self.window.geometry("480x320")
        tk.Label(self.window, text="Add Watermark to Video", font=("Arial", 13, "bold")).pack(pady=10)
        tk.Label(self.window, text="Video file:").pack()
        self.video_entry = tk.Entry(self.window, width=55); self.video_entry.pack()
        tk.Button(self.window, text="Browse Video", command=lambda: self.browse(self.video_entry, [("Video Files","*.mp4 *.avi *.mov *.mkv")])).pack(pady=3)
        tk.Label(self.window, text="Watermark image:").pack()
        self.wm_entry = tk.Entry(self.window, width=55); self.wm_entry.pack()
        tk.Button(self.window, text="Browse Image", command=lambda: self.browse(self.wm_entry, [("Images","*.png *.jpg *.jpeg")])).pack(pady=3)
        tk.Label(self.window, text="Opacity (0.1 - 1.0):").pack()
        self.opacity_var = tk.StringVar(value="0.5")
        tk.Entry(self.window, textvariable=self.opacity_var, width=10).pack()
        tk.Button(self.window, text="Add Watermark", bg="#9C27B0", fg="white", command=self.run_watermark).pack(pady=10)
        self.status = tk.Label(self.window, text="", wraplength=420, fg="green"); self.status.pack()
    def browse(self, entry: tk.Entry, types: list[tuple[str, str]]) -> None:
        p = filedialog.askopenfilename(filetypes=types)
        if p:
            entry.delete(0, tk.END); entry.insert(0, p)
    def run_watermark(self):
        v, w = self.video_entry.get().strip(), self.wm_entry.get().strip()
        if not v or not w:
            messagebox.showwarning("Missing", "Select both video and watermark image"); return
        try:
            out = os.path.splitext(v)[0] + "_watermarked.mp4"
            self.status.config(text="Processing..."); self.window.update()
            add_watermark(v, w, out, float(self.opacity_var.get() or 0.5))
            self.status.config(text="Saved as: " + out)
        except Exception as e:
            messagebox.showerror("Error", str(e)); self.status.config(text="Error: "+str(e))
    def run(self): self.window.mainloop()

def open_window(parent: tk.Misc | None = None) -> WatermarkTool: return WatermarkTool(parent)
if __name__ == "__main__": WatermarkTool().run()
