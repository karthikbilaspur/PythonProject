"""
Employee QR Generator - Medium Level
Fixes: validates + sanitizes Employee ID for filename, JSON data in QR (not fragile plain text),
proper image keep-alive, clear resets image, no fixed-size-only layout issues.
Requires: pip install qrcode pillow python-resize-image
"""
import json, re, tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import cast
import qrcode
from PIL import Image, ImageOps, ImageTk

OUT = Path("employee_qr"); OUT.mkdir(exist_ok=True)
ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,30}$")

class App:
    def __init__(self, root: tk.Tk):
        self.root=root; root.title("Employee QR Generator"); root.geometry("900x500"); root.resizable(False, False)
        self.emp_id=tk.StringVar(); self.name=tk.StringVar(); self.dept=tk.StringVar(); self.desig=tk.StringVar()
        left=ttk.Frame(root, padding=16); left.place(x=40, y=90, width=500, height=380)
        ttk.Label(left, text="Employee Details", font=("Helvetica",16,"bold")).pack(anchor="w", pady=5)
        for label, var in [("Employee ID", self.emp_id), ("Name", self.name), ("Department", self.dept), ("Designation", self.desig)]:
            ttk.Label(left, text=label).pack(anchor="w")
            ttk.Entry(left, textvariable=var, width=50).pack(fill="x", pady=3)
        btns=ttk.Frame(left); btns.pack(pady=10)
        ttk.Button(btns, text="Generate QR", command=self.generate).pack(side="left", padx=4)
        ttk.Button(btns, text="Clear", command=self.clear).pack(side="left", padx=4)
        self.msg=ttk.Label(left, text=""); self.msg.pack(pady=5)
        right=ttk.Frame(root, padding=12); right.place(x=580, y=90, width=280, height=380)
        ttk.Label(right, text="Employee QR Code", font=("Helvetica",13,"bold")).pack()
        self.qr_label=ttk.Label(right, text="No QR\navailable", justify="center"); self.qr_label.pack(pady=20)
        self.path_label=ttk.Label(right, text="", wraplength=240); self.path_label.pack()
        self.photo=None
    def clear(self):
        for v in (self.emp_id, self.name, self.dept, self.desig): v.set("")
        self.msg.config(text=""); self.qr_label.config(image="", text="No QR\navailable"); self.photo=None; self.path_label.config(text="")
    def generate(self):
        emp, name, dept, desig = (v.get().strip() for v in (self.emp_id, self.name, self.dept, self.desig))
        if not all([emp, name, dept, desig]): self.msg.config(text="All fields required!", foreground="red"); return
        if not ID_RE.match(emp): self.msg.config(text="Employee ID: only letters, numbers, _ - (max 30)", foreground="red"); return
        data=json.dumps({"employee_id":emp,"name":name,"department":dept,"designation":desig}, ensure_ascii=False)
        try:
            img=ImageOps.fit(cast(Image.Image, qrcode.make(data)), (180, 180))
            path=OUT / f"emp_{emp}.png"; img.save(path)
            pil=Image.open(path).resize((180,180)); self.photo=ImageTk.PhotoImage(pil)
            self.qr_label.config(image=self.photo, text=""); self.msg.config(text="QR generated successfully!", foreground="green"); self.path_label.config(text=f"Saved: {path}")
        except Exception as e: messagebox.showerror("Error", str(e))

if __name__=="__main__":
    root=tk.Tk(); App(root); root.mainloop()
