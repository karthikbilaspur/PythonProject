"""
Pwned Password Checker - Medium Level
Features: HIBP k-anonymity (only first 5 chars of SHA-1 sent),
password strength meter, show/hide, history-free (never stores password),
timeout + error handling, Enter-key support, copy-safe UI.
"""
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "https://api.pwnedpasswords.com/range/{}"
HEADERS = {"User-Agent": "PwnedChecker-Medium-Demo"}

def sha1_split(password: str):
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return digest[:5], digest[5:]

def check_pwned(password: str) -> int:
    prefix, suffix = sha1_split(password)
    resp = requests.get(API_URL.format(prefix), headers=HEADERS, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"HIBP API returned {resp.status_code}")
    for line in resp.text.splitlines():
        h, count = line.split(":")
        if h == suffix: return int(count)
    return 0

def strength(password: str) -> tuple[str, int]:
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(not c.isalnum() for c in password): score += 1
    labels = ["Very Weak","Weak","Fair","Good","Strong","Very Strong","Excellent"]
    return labels[min(score, 6)], int(score / 6 * 100)

class App:
    def __init__(self, root):
        self.root = root; root.title("Pwned Password Checker"); root.geometry("440x340"); root.resizable(False, False)
        frm = ttk.Frame(root, padding=16); frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Check if your password leaked", font=("Helvetica", 14, "bold")).pack(pady=5)
        ttk.Label(frm, text="Your full password is NEVER sent. Only the first 5 chars of its SHA-1 hash are sent (k-anonymity).", wraplength=400, justify="center").pack(pady=5)
        self.var = tk.StringVar()
        self.entry = ttk.Entry(frm, textvariable=self.var, show="*", width=40, font=("Helvetica", 12)); self.entry.pack(pady=8); self.entry.bind("<Return>", lambda e: self.check())
        row = ttk.Frame(frm); row.pack()
        self.toggle_btn = ttk.Button(row, text="Show", command=self.toggle); self.toggle_btn.pack(side="left", padx=4)
        ttk.Button(row, text="Check Password", command=self.check).pack(side="left", padx=4)
        ttk.Button(row, text="Clear", command=self.clear).pack(side="left", padx=4)
        self.strength_label = ttk.Label(frm, text="Strength: -"); self.strength_label.pack(pady=4)
        self.bar = ttk.Progressbar(frm, length=300, mode="determinate"); self.bar.pack()
        self.result = ttk.Label(frm, text="", wraplength=400, justify="center", font=("Helvetica", 11)); self.result.pack(pady=10)
        ttk.Label(frm, text="Tip: Use a password manager + unique password per site.", wraplength=400, justify="center").pack()
        self.entry.focus()

    def toggle(self):
        show = self.entry.cget("show") == "*"
        self.entry.config(show="" if show else "*"); self.toggle_btn.config(text="Hide" if show else "Show")
    def clear(self): self.var.set(""); self.result.config(text=""); self.strength_label.config(text="Strength: -"); self.bar["value"] = 0
    def check(self):
        pw = self.var.get()
        if not pw: messagebox.showerror("Error", "Please enter a password"); return
        if len(pw) < 4: messagebox.showwarning("Too short", "Password is too short to be safe."); return
        label, pct = strength(pw); self.strength_label.config(text=f"Strength: {label}"); self.bar["value"] = pct
        self.result.config(text="Checking...", foreground="black"); self.root.update()
        try: count = check_pwned(pw)
        except requests.RequestException: messagebox.showerror("Network", "Could not reach HIBP API. Check internet."); self.result.config(text=""); return
        except Exception as e: messagebox.showerror("Error", str(e)); return
        if count: self.result.config(text=f"⚠️ Found {count:,} times in breaches!\nChange it immediately. Use a unique password.", foreground="red")
        else: self.result.config(text=f"✅ Not found in known breaches.\nStill use a strong, unique password.", foreground="green")
        self.var.set("")  # never keep password in memory

if __name__ == "__main__":
    root = tk.Tk(); App(root); root.mainloop()
