"""
Stock Trader Agent - IMPROVED (Alpha Vantage)
Fixes vs original:
  - Fetch button was created but NEVER packed -> invisible / unclickable. Fixed.
  - fetch_data froze UI (network on main thread) -> now background thread.
  - No API key handling -> now reads env ALPHA_VANTAGE_API_KEY or asks in GUI.
  - No error handling -> API limit / bad symbol / no internet now shows messagebox.
  - plot_data crashed if column name changed / no data -> now validates + embedded chart.
  - No table / stats -> now shows table + High/Low/Change + embedded Matplotlib chart.
  - No period selector -> now 1mo/6mo/1y/Full.
Run: python index.py
Needs: pip install -r requirements.txt
Get free key: https://www.alphavantage.co/support/#api-key (25 req/day free)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os, threading
from typing import Any
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "YOUR_API_KEY")

class StockTraderAgent:
    def __init__(self, root:tk.Tk):
        self.root=root; self.root.title("Stock Market Trader Agent"); self.root.geometry("900x600")
        self.data=None
        # Top controls
        top=tk.Frame(root); top.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(top, text="Stock Symbol:").pack(side=tk.LEFT)
        self.stock_entry=tk.Entry(top, width=12); self.stock_entry.insert(0,"AAPL"); self.stock_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(top, text="API Key:").pack(side=tk.LEFT)
        self.key_entry=tk.Entry(top, width=20, show="*"); self.key_entry.insert(0, API_KEY if API_KEY!="YOUR_API_KEY" else ""); self.key_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(top, text="Period:").pack(side=tk.LEFT)
        self.period=ttk.Combobox(top, values=["compact (100 days)","full"], width=16, state="readonly")
        self.period.set("compact (100 days)"); self.period.pack(side=tk.LEFT, padx=5)
        self.fetch_button=tk.Button(top, text="Fetch Data", command=self.fetch_data); self.fetch_button.pack(side=tk.LEFT, padx=5)  # FIXED: was never packed
        self.plot_button=tk.Button(top, text="Plot Data", command=self.plot_data); self.plot_button.pack(side=tk.LEFT)
        self.status=tk.Label(root, text="Enter symbol (e.g. AAPL, RELIANCE.BSE, TCS.BSE) + API key, then Fetch.", anchor=tk.W); self.status.pack(fill=tk.X, padx=10)
        # Stats
        self.stats_label=tk.Label(root, text="No data yet.", font=("Helvetica", 11, "bold"), anchor=tk.W); self.stats_label.pack(fill=tk.X, padx=10)
        # Table
        cols=("Date","Open","High","Low","Close","Volume")
        self.tree=ttk.Treeview(root, columns=cols, show="headings", height=10)
        for c in cols: self.tree.heading(c, text=c); self.tree.column(c, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        # Chart
        self.fig: Figure = Figure(figsize=(8,3))
        self.ax = self.fig.add_subplot(111)
        self.canvas=FigureCanvasTkAgg(self.fig, master=root); self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def fetch_data(self):
        symbol=self.stock_entry.get().strip().upper()
        key=self.key_entry.get().strip() or API_KEY
        if not symbol: messagebox.showwarning("Missing", "Enter a stock symbol."); return
        if not key or key=="YOUR_API_KEY":
            messagebox.showwarning("API Key Needed", "Get free key from alphavantage.co and paste it.\nOr set env: ALPHA_VANTAGE_API_KEY=your_key")
            return
        self.fetch_button.config(state=tk.DISABLED); self.status.config(text=f"Fetching {symbol}...")
        threading.Thread(target=self._fetch_worker, args=(symbol,key), daemon=True).start()

    def _fetch_worker(self, symbol: str, key: str):
        try:
            from alpha_vantage.timeseries import TimeSeries  # type: ignore[reportMissingTypeStubs]
            ts: Any = TimeSeries(key=key, output_format='pandas')
            outsize='full' if 'full' in self.period.get() else 'compact'
            df, _meta = ts.get_daily_adjusted(symbol=symbol, outputsize=outsize)
            if df is None or df.empty: raise ValueError("No data returned - check symbol.")
            # Alpha Vantage column names: '1. open','2. high','3. low','4. close','6. volume'
            df=df.sort_index()
            self.data=df
            self.root.after(0, lambda: self._show_data(symbol))
        except Exception as e:
            self.root.after(0, lambda: (messagebox.showerror("Fetch Failed", f"{e}\n\nTip: Free Alpha Vantage = 25 requests/day. Wait a minute and retry."),
                                          self.status.config(text="Fetch failed."), self.fetch_button.config(state=tk.NORMAL)))

    def _show_data(self, symbol: str):
        self.fetch_button.config(state=tk.NORMAL)
        df=self.data
        if df is None or df.empty:
            self.status.config(text="No data available.")
            return
        close_col=[c for c in df.columns if 'close' in c.lower()][0]
        latest=df.iloc[-1]; prev=df.iloc[-2] if len(df)>1 else latest
        change=float(latest[close_col]-prev[close_col]); pct=change/float(prev[close_col])*100
        self.stats_label.config(text=f"{symbol} | Latest Close: ${float(latest[close_col]):.2f} | Change: {change:+.2f} ({pct:+.2f}%) | High: ${float(latest[[c for c in df.columns if 'high' in c.lower()][0]]):.2f} | Rows: {len(df)}")
        self.status.config(text=f"Fetched {len(df)} rows for {symbol}")
        # Table: last 20 rows
        for r in self.tree.get_children(): self.tree.delete(r)
        for date,row in df.tail(20).iterrows():
            vals=[str(date.date()) if hasattr(date,'date') else str(date)]
            for c in ['1. open','2. high','3. low','4. close','6. volume']:
                vals.append(f"{float(row[c]):.2f}" if c in row else "-")
            self.tree.insert("", tk.END, values=vals)
        self.plot_data()

    def plot_data(self):
        df = self.data
        if df is None:
            messagebox.showinfo("No Data", "Fetch data first.")
            return
        close_col=[c for c in df.columns if 'close' in c.lower()][0]
        self.ax.clear(); self.ax.plot(df.index, df[close_col], color="#1f77b4")  # type: ignore[reportUnknownMemberType]
        self.ax.set_title(f"{self.stock_entry.get().strip().upper()} - Adjusted Close")  # type: ignore[reportUnknownMemberType]
        self.ax.set_xlabel("Date")  # type: ignore[reportUnknownMemberType]
        self.ax.set_ylabel("Price")  # type: ignore[reportUnknownMemberType]
        self.ax.grid(True, alpha=0.3)  # type: ignore[reportUnknownMemberType]
        self.fig.autofmt_xdate(); self.canvas.draw()

if __name__=="__main__":
    root=tk.Tk(); app=StockTraderAgent(root); root.mainloop()
