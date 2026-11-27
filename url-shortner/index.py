import argparse
import hashlib
import sqlite3
import urllib.parse
from datetime import datetime

BASE_URL = "http://short.local/"
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class URLShortener:
    def __init__(self, db_name: str = "urls.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                short_code TEXT PRIMARY KEY,
                original_url TEXT UNIQUE,
                created_at TEXT,
                clicks INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def _normalize(self, url: str) -> str:
        url = url.strip()
        if not url:
            raise ValueError("URL cannot be empty.")
        if " " in url:
            raise ValueError("URL cannot contain spaces.")
        # Add scheme if user typed "example.com/page"
        if "://" not in url:
            url = "https://" + url
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(f"Not a valid URL: {url!r}")
        return url

    def _make_code(self, url: str, attempt: int = 0) -> str:
        # Hash + attempt salt, then map to base62 for shorter codes
        digest = hashlib.sha256(f"{url}|{attempt}".encode()).digest()
        num = int.from_bytes(digest[:6], "big")
        code = ""
        while num > 0:
            num, rem = divmod(num, 62)
            code = CHARS[rem] + code
        return (code or "0")[:7]

    def shorten_url(self, original_url: str) -> str:
        url = self._normalize(original_url)
        # Same URL -> same code, no crash
        row = self.conn.execute(
            "SELECT short_code FROM urls WHERE original_url = ?", (url,)
        ).fetchone()
        if row:
            return row[0]
        # Different URL, same code -> retry with salt
        attempt = 0
        while True:
            code = self._make_code(url, attempt)
            try:
                self.conn.execute(
                    "INSERT INTO urls (short_code, original_url, created_at) VALUES (?, ?, ?)",
                    (code, url, datetime.now().isoformat(timespec="seconds")),
                )
                self.conn.commit()
                return code
            except sqlite3.IntegrityError:
                # Code taken by a different URL (collision) -> try next salt
                attempt += 1

    def get_original_url(self, short_code: str) -> str | None:
        code = short_code.strip().removeprefix(BASE_URL).removeprefix("short.local/").split("/")[-1]
        row = self.conn.execute(
            "SELECT original_url FROM urls WHERE short_code = ?", (code,)
        ).fetchone()
        if not row:
            return None
        self.conn.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (code,)
        )
        self.conn.commit()
        return row[0]

    def stats(self, short_code: str):
        return self.conn.execute(
            "SELECT original_url, created_at, clicks FROM urls WHERE short_code = ?",
            (short_code.strip(),),
        ).fetchone()

    def list_all(self):
        return self.conn.execute(
            "SELECT short_code, original_url, clicks FROM urls ORDER BY created_at DESC"
        ).fetchall()


def run_cli():
    s = URLShortener()
    try:
        while True:
            print("\n1. Shorten URL")
            print("2. Get Original URL")
            print("3. Stats")
            print("4. List all")
            print("5. Quit")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                try:
                    code = s.shorten_url(input("Enter the URL to shorten: "))
                    print(f"Short URL: {BASE_URL}{code}  (code: {code})")
                except ValueError as e:
                    print(f"Error: {e}")
            elif choice == "2":
                url = s.get_original_url(input("Enter short code or URL: "))
                print(f"Original URL: {url}" if url else "URL not found")
            elif choice == "3":
                row = s.stats(input("Enter short code: "))
                print(f"Original: {row[0]}\nCreated: {row[1]}\nClicks: {row[2]}" if row else "Not found")
            elif choice == "4":
                for code, url, clicks in s.list_all():
                    print(f"{BASE_URL}{code} -> {url} ({clicks} clicks)")
            elif choice == "5":
                break
            else:
                print("Invalid choice")
    finally:
        s.close()


def run_gui():
    import tkinter as tk
    from tkinter import messagebox

    s = URLShortener()
    window = tk.Tk()
    window.title("URL Shortener (Local)")
    window.geometry("520x260")

    tk.Label(window, text="Enter URL:").pack(pady=(12, 0))
    entry = tk.Entry(window, width=60)
    entry.pack(pady=5)

    result = tk.Label(window, text="", wraplength=480, fg="blue")
    result.pack(pady=8)
    state = {"code": ""}

    def do_shorten():
        try:
            code = s.shorten_url(entry.get())
            state["code"] = code
            result.config(text=f"Short URL: {BASE_URL}{code}")
            copy_btn.config(state="normal")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

    def do_copy():
        window.clipboard_clear()
        window.clipboard_append(f"{BASE_URL}{state['code']}")
        messagebox.showinfo("Copied", "Short URL copied to clipboard!")

    def do_expand():
        url = s.get_original_url(entry.get())
        if url:
            messagebox.showinfo("Original URL", url)
        else:
            messagebox.showerror("Error", "Short code not found")

    tk.Button(window, text="Shorten URL", command=do_shorten).pack(pady=3)
    tk.Button(window, text="Expand Short Code", command=do_expand).pack(pady=3)
    copy_btn = tk.Button(window, text="Copy to Clipboard", command=do_copy, state="disabled")
    copy_btn.pack(pady=3)

    def on_close():
        s.close()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gui", action="store_true", help="Launch Tkinter GUI")
    args = parser.parse_args()
    if args.gui:
        run_gui()
    else:
        run_cli()