"""
pip install qrcode pillow
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image, ImageTk
from pathlib import Path

BG="#1E1E1E"; FG="white"
class App:
    def __init__(self, root: tk.Tk):
        self.root=root; root.title("QR Code Generator"); root.configure(bg=BG); root.geometry("480x560")
        self.photo=None; self.last_path=Path("qr_code.png")
        ttk.Label(root, text="Enter data for QR code:", background=BG, foreground=FG, font=("Helvetica",12)).pack(pady=8)
        self.entry=ttk.Entry(root, width=45, font=("Helvetica",12)); self.entry.pack(pady=4)
        btns=ttk.Frame(root); btns.pack(pady=8)
        ttk.Button(btns, text="Generate", command=self.generate).pack(side="left", padx=4)
        ttk.Button(btns, text="Save As...", command=self.save).pack(side="left", padx=4)
        ttk.Button(btns, text="Clear", command=self.clear).pack(side="left", padx=4)
        self.preview=tk.Label(root, bg=BG, fg=FG, text="No QR yet"); self.preview.pack(pady=8)
        self.status=tk.Label(root, bg=BG, fg=FG, text="", wraplength=420); self.status.pack()
        self.entry.focus()

    def build(self, data: str, path: Path) -> Path:
        qr=qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_M, box_size=10, border=4)
        qr.add_data(data); qr.make(fit=True)
        img=qr.make_image(fill_color="black", back_color="white"); img.save(str(path)); return path
    
    def show(self, path: Path):
        img=Image.open(path); img.thumbnail((260,260)); self.photo=ImageTk.PhotoImage(img)
        self.preview.config(image=self.photo, text="")
    def generate(self):
        data=self.entry.get().strip()
        if not data: messagebox.showerror("Error","Enter some data first"); self.status.config(text=""); return
        try: self.build(data, self.last_path); self.show(self.last_path); self.status.config(text="QR generated. Use Save As to choose a location.")
        except Exception as e: messagebox.showerror("Error", f"Failed: {e}")
    def save(self):
        data=self.entry.get().strip()
        if not data: messagebox.showerror("Error","Enter data first"); return
        p=filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png")])
        if not p: self.status.config(text="Save cancelled."); return
        try: self.build(data, Path(p)); self.last_path=Path(p); self.show(self.last_path); self.status.config(text=f"Saved to: {p}")
        except Exception as e: messagebox.showerror("Error", str(e))
    def clear(self): self.entry.delete(0,"end"); self.preview.config(image="", text="No QR yet"); self.photo=None; self.status.config(text="")

if __name__=="__main__":
    root=tk.Tk(); App(root); root.mainloop()
