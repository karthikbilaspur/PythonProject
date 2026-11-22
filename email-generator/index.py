"""
QR Generator + Email - Medium Level
Fixes: no hardcoded credentials, env vars / app password, validation,
proper error messages, preview + save + send in one flow, no bare except.
Requires: pip install pyqrcode pypng pillow
Set env: QR_SENDER_EMAIL, QR_SENDER_APP_PASSWORD
"""
import os, re, smtplib, ssl
from email.message import EmailMessage
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyqrcode  # type: ignore[import-untyped]
from PIL import Image, ImageTk

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root=root; root.title("QR Code Generator + Email"); root.geometry("520x560")
        self.qr_path=None; self.photo=None
        f=ttk.Frame(root, padding=14); f.pack(fill="both", expand=True)
        ttk.Label(f, text="Text / URL:").pack(anchor="w")
        self.data=ttk.Entry(f, width=60); self.data.pack(fill="x", pady=4)
        ttk.Label(f, text="Recipient email (for Send):").pack(anchor="w")
        self.email=ttk.Entry(f, width=60); self.email.pack(fill="x", pady=4)
        btns=ttk.Frame(f); btns.pack(pady=8)
        ttk.Button(btns, text="Generate", command=self.generate).pack(side="left", padx=4)
        ttk.Button(btns, text="Save PNG", command=self.save).pack(side="left", padx=4)
        ttk.Button(btns, text="Send Email", command=self.send).pack(side="left", padx=4)
        self.preview=ttk.Label(f, text="No QR yet"); self.preview.pack(pady=8)
        self.status=ttk.Label(f, text=""); self.status.pack()
        ttk.Label(f, text="Note: Email uses env vars QR_SENDER_EMAIL + QR_SENDER_APP_PASSWORD (Gmail App Password, not normal password).", wraplength=480).pack(pady=8)

    def make_qr(self, text: str, path: Path) -> None:
        qr=pyqrcode.create(text); qr.png(str(path), scale=8)  # pyright: ignore[reportUnknownMemberType]
    def generate(self):
        text=self.data.get().strip()
        if not text: messagebox.showerror("Error","Enter text / URL first"); return
        try:
            tmp=Path("qr_preview.png"); self.make_qr(text, tmp); self.qr_path=tmp
            img=Image.open(tmp).resize((260,260)); self.photo=ImageTk.PhotoImage(img)
            self.preview.config(image=self.photo, text=""); self.status.config(text=f"QR for: {text[:60]}")
        except Exception as e: messagebox.showerror("Error", f"Failed to generate QR: {e}")
    def save(self):
        if not self.data.get().strip(): messagebox.showerror("Error","Generate first"); return
        p=filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png")])
        if not p: return
        try: self.make_qr(self.data.get().strip(), Path(p)); self.status.config(text=f"Saved to {p}")
        except Exception as e: messagebox.showerror("Error", str(e))
    def send(self):
        to=self.email.get().strip()
        if not EMAIL_RE.match(to): messagebox.showerror("Error","Enter a valid email"); return
        if not self.qr_path or not self.qr_path.exists(): messagebox.showerror("Error","Generate QR first"); return
        sender=os.getenv("QR_SENDER_EMAIL"); pwd=os.getenv("QR_SENDER_APP_PASSWORD")
        if not sender or not pwd: messagebox.showerror("Missing config","Set QR_SENDER_EMAIL and QR_SENDER_APP_PASSWORD env vars"); return
        try:
            msg=EmailMessage(); msg["Subject"]="Your QR Code"; msg["From"]=sender; msg["To"]=to
            msg.set_content(f"QR code for: {self.data.get().strip()}")
            msg.add_attachment(self.qr_path.read_bytes(), maintype="image", subtype="png", filename=self.qr_path.name)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as s:
                s.login(sender, pwd); s.send_message(msg)
            messagebox.showinfo("Sent", f"Mail sent to {to}")
        except Exception as e: messagebox.showerror("Email failed", str(e))

if __name__=="__main__":
    root=tk.Tk(); App(root); root.mainloop()
