import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable, cast
import threading
import requests
import pandas as pd

# 【entity-NSE¦canonical_name=NSE】 blocks requests without proper headers + cookies
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}

# Category -> (api_url, columns to show)
CATEGORIES = {
    "Most Active - By Value": (
        "https://www.nseindia.com/api/live-analysis/most-active-securities?index=value",
        ["symbol", "lastPrice", "pChange", "totalTradedValue", "totalTradedVolume"]
    ),
    "Most Active - By Volume": (
        "https://www.nseindia.com/api/live-analysis/most-active-securities?index=volume",
        ["symbol", "lastPrice", "pChange", "totalTradedVolume", "totalTradedValue"]
    ),
    "NIFTY 50 - Top Gainers": (
        "https://www.nseindia.com/api/live-analysis/variations?index=gainers",
        ["symbol", "lastPrice", "pChange", "open", "dayHigh", "dayLow"]
    ),
    "NIFTY 50 - Top Losers": (
        "https://www.nseindia.com/api/live-analysis/variations?index=losers",
        ["symbol", "lastPrice", "pChange", "open", "dayHigh", "dayLow"]
    ),
    "Price Spurts - NIFTY 500": (
        "https://www.nseindia.com/api/live-analysis/price-spurts?index=NIFTY%20500",
        ["symbol", "lastPrice", "pChange", "lastCorpAnnouncement", "lastCorpAnnouncementDate"]
    ),
    "Volume Spurts - NIFTY 500": (
        "https://www.nseindia.com/api/live-analysis/volume-spurts?index=NIFTY%20500",
        ["symbol", "lastPrice", "pChange", "totalTradedVolume", "avgTradedVolume"]
    ),
}

# Pretty column names
COLUMN_LABELS = {
    "symbol": "Symbol",
    "lastPrice": "LTP",
    "pChange": "% Change",
    "open": "Open",
    "dayHigh": "High",
    "dayLow": "Low",
    "totalTradedValue": "Traded Value (Cr)",
    "totalTradedVolume": "Volume",
    "avgTradedVolume": "Avg Volume",
    "lastCorpAnnouncement": "Announcement",
    "lastCorpAnnouncementDate": "Date",
}

class NSEApp:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("NSE Live Market Data")
        self.root.geometry("1100x650")
        self.root.configure(bg="white")

        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.df = pd.DataFrame()
        self.is_loading = False

        self._build_ui()
        # Get cookies once on startup in background
        threading.Thread(target=self._init_session, daemon=True).start()

    def _build_ui(self):
        # --- Top bar ---
        top = ttk.Frame(self.root, padding=12)
        top.pack(fill="x")

        ttk.Label(top, text="NSE Live Market Data",
                  font=("Helvetica", 20, "bold")).pack(side="left")

        ttk.Label(top, text="Category:", font=("Helvetica", 11)).pack(side="left", padx=(20, 5))

        self.category_var = tk.StringVar(value=list(CATEGORIES.keys())[0])
        self.combo = ttk.Combobox(top, textvariable=self.category_var,
                                  values=list(CATEGORIES.keys()),
                                  state="readonly", width=32, font=("Helvetica", 11))
        self.combo.pack(side="left")

        self.fetch_btn = ttk.Button(top, text="Get Stock Data", command=self.fetch_data)
        self.fetch_btn.pack(side="left", padx=10)

        self.export_btn = ttk.Button(top, text="Export CSV", command=self.export_csv, state="disabled")
        self.export_btn.pack(side="left")

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var,
                  font=("Helvetica", 10, "italic")).pack(anchor="w", padx=12)

        # --- Table ---
        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.pack(fill="both", expand=True, padx=12, pady=(5, 12))

        # Scrollbars
        vsb = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=cast(Callable[..., None], self.tree.yview),
        )
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(
            self.root,
            orient="horizontal",
            command=lambda *args: self.tree.xview(*args),
        )
        hsb.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=hsb.set)

        # Style: green for gainers, red for losers
        self.tree.tag_configure("up", foreground="#0a7a42")
        self.tree.tag_configure("down", foreground="#c62828")

    def _init_session(self):
        """NSE requires a homepage visit first to set cookies."""
        try:
            self.session.get("https://www.nseindia.com", timeout=10)
        except Exception:
            pass

    def fetch_data(self):
        if self.is_loading:
            return
        self.is_loading = True
        self.fetch_btn.config(state="disabled")
        self.status_var.set(f"Fetching {self.category_var.get()}...")
        threading.Thread(target=self._fetch_worker, daemon=True).start()

    def _fetch_worker(self):
        category = self.category_var.get()
        url, cols = CATEGORIES[category]

        try:
            # Retry once if session expired (NSE cookies expire fast)
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 401:
                self._init_session()
                resp = self.session.get(url, timeout=15)
            resp.raise_for_status()

            data = resp.json().get("data", [])
            if not data:
                raise ValueError("No data returned. NSE may be closed or blocking requests.")

            df = pd.DataFrame(data)

            # Keep only columns that exist, in order
            cols = [c for c in cols if c in df.columns]
            df = df[cols].copy()

            # Clean numbers: format value in Cr
            if "totalTradedValue" in df.columns:
                df["totalTradedValue"] = (df["totalTradedValue"] / 1e7).round(2)

            for col in ["lastPrice", "pChange", "open", "dayHigh", "dayLow"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

            self.df = df
            self.root.after(0, self._update_table, cols)

        except Exception as e:
            self.root.after(0, self._on_error, str(e))

    def _update_table(self, cols: list[str]):
        # Clear old columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cols

        for col in cols:
            self.tree.heading(col, text=COLUMN_LABELS.get(col, col))
            self.tree.column(col, width=150, anchor="center")
        self.tree.column(cols[0], width=180, anchor="w")

        for _, row in self.df.iterrows():
            values = [row[c] for c in cols]
            tag = ""
            if "pChange" in self.df.columns:
                try:
                    tag = "up" if float(row["pChange"]) >= 0 else "down"
                except:
                    pass
            self.tree.insert("", "end", values=values, tags=(tag,))

        self.status_var.set(f"Showing {len(self.df)} rows • {self.category_var.get()}")
        self.export_btn.config(state="normal")
        self._finish()

    def _on_error(self, msg: str):
        messagebox.showerror("Error", f"Failed to fetch data:\n{msg}\n\nTip: NSE blocks too many requests. Wait 30 sec and try again.")
        self.status_var.set("Error - try again")
        self._finish()

    def _finish(self):
        self.is_loading = False
        self.fetch_btn.config(state="normal")

    def export_csv(self):
        if self.df.empty:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile=f"nse_{self.category_var.get().replace(' ', '_').lower()}.csv"
        )
        if path:
            self.df.to_csv(path, index=False)
            messagebox.showinfo("Saved", f"Saved to {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NSEApp(root)
    root.mainloop()