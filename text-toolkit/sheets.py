import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

CREDENTIALS_FILE = os.environ.get("GOOGLE_CREDENTIALS_JSON", "credentials.json")
SHEET_NAME = "Sheet Name"

def _connect():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as e:
        raise RuntimeError(f"Missing library: {e}. Install with: pip install gspread google-auth")
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_FILE}\nDownload a service-account JSON from Google Cloud and place it here.")
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(  # pyright: ignore[reportUnknownMemberType]
        CREDENTIALS_FILE, scopes=scopes
    )
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

def open_sheets_window(parent: tk.Misc):
    win = tk.Toplevel(parent)
    win.title("Text to Sheets")
    win.geometry("520x480")
    tk.Label(win, text=f"Sheet: {SHEET_NAME}  |  Credentials: {CREDENTIALS_FILE}", wraplength=480, fg="gray").pack(pady=5)
    tk.Label(win, text="Enter text:").pack()
    entry = scrolledtext.ScrolledText(win, height=6, width=55)
    entry.pack(padx=10, pady=5)

    def write_text():
        text = entry.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showerror("Error", "Please enter text!")
            return
        try:
            sheet = _connect()
            sheet.append_row([text])
            messagebox.showinfo("Success", "Text written to sheet successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_text():
        try:
            sheet = _connect()
            data = sheet.get_all_records()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        if not data:
            messagebox.showinfo("Sheet Data", "No data in sheet!")
            return
        top = tk.Toplevel(win)
        top.title("Sheet Data")
        top.geometry("500x400")
        txt = scrolledtext.ScrolledText(top, width=60, height=20)
        txt.pack(padx=10, pady=10)
        for row in data:
            txt.insert(tk.END, str(row) + "\n")

    def clear_text():
        if not messagebox.askyesno("Clear Sheet", "Are you sure you want to clear the sheet?"):
            return
        try:
            sheet = _connect()
            sheet.clear()
            messagebox.showinfo("Success", "Sheet cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Write to Sheet", command=write_text).pack(pady=4)
    tk.Button(win, text="Read from Sheet", command=read_text).pack(pady=4)
    tk.Button(win, text="Clear Sheet", command=clear_text).pack(pady=4)
    tk.Label(win, text="Tip: Share your Google Sheet with the service-account email\nshown inside credentials.json, or writes will fail.", fg="gray", justify="center").pack(pady=10)
