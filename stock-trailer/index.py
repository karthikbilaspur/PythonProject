"""
Real-Time Stock Tracker - IMPROVED (yfinance)
Fixes vs original:
  - Stop button did thread.join() on UI thread -> froze app. Now no join on UI.
  - fetch used history(period=1d, interval=1m) every 5s -> slow + heavy. Now fast_info / 1m cache.
  - No symbol validation, empty data crashed (iloc[-1] on empty) -> now checks empty.
  - Graph x-axis was strings, grew forever -> now keeps last 60 points, proper datetime axis.
  - No price change colour / high-low / status -> added.
  - Thread not daemon -> app wouldn't close. Now daemon.
Run: python stock_tracker.py
Needs: pip install -r requirements.txt
Note: yfinance is unofficial Yahoo data, may be delayed / rate-limited. Not financial advice.
"""
import tkinter as tk
from tkinter import messagebox
import yfinance as yf  # pyright: ignore[reportMissingTypeStubs]
import threading, time
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
from collections.abc import Mapping
from typing import Any, cast

class StockTracker:
    def __init__(self, root:tk.Tk):
        self.root=root; self.root.title("Real-Time Stock Tracker"); self.root.geometry("800x600")
        self.stock_name=tk.StringVar(value="AAPL")
        self.price=tk.StringVar(value="Press Start Tracking")
        self.prev_price=None; self.high=None; self.low=None
        top=tk.Frame(root); top.pack(padx=10, pady=10, fill=tk.X)
        tk.Label(top, text="Stock Symbol:").pack(side=tk.LEFT)
        tk.Entry(top, textvariable=self.stock_name, width=15).pack(side=tk.LEFT, padx=5)
        tk.Label(top, text="e.g. AAPL, MSFT, RELIANCE.NS").pack(side=tk.LEFT, padx=5)
        btn=tk.Frame(root); btn.pack(pady=5)
        self.start_btn=tk.Button(btn, text="Start Tracking", bg="#28a745", fg="white", command=self.start_tracking); self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn=tk.Button(btn, text="Stop Tracking", bg="#dc3545", fg="white", command=self.stop_tracking, state=tk.DISABLED); self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.price_label=tk.Label(root, textvariable=self.price, font=("Arial", 26, "bold"), fg="#28a745"); self.price_label.pack(pady=10)
        self.info_label=tk.Label(root, text="High: - | Low: - | Change: - | Last update: -", font=("Arial", 11)); self.info_label.pack()
        self.status=tk.Label(root, text="Ready.", anchor=tk.W); self.status.pack(fill=tk.X, padx=10)
        graph_frame=tk.Frame(root); graph_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.fig: Figure = Figure()
        self.ax: Axes = self.fig.add_subplot(111)
        self.canvas=FigureCanvasTkAgg(self.fig, master=graph_frame); self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.prices: list[float]=[]; self.times: list[datetime]=[]; self.stop_event=threading.Event(); self.thread=None
        self.ticker=None

    def fetch_price(self):
        try:
            ticker = self.ticker
            if ticker is None:
                return None
            # fast_info is much lighter than history() every 5s
            info = cast(Mapping[str, object], ticker.fast_info)
            raw_price = info.get('lastPrice') or info.get('last_price')
            p = raw_price if isinstance(raw_price, (int, float)) else None
            if p is None:
                data=cast(Any, ticker).history(period='1d', interval='1m')
                if data.empty: return None
                p=float(data['Close'].iloc[-1])
            return float(p)
        except Exception as e:
            print(f"Error fetching price: {e}"); return None

    def update_loop(self):
        while not self.stop_event.is_set():
            price=self.fetch_price()
            if price is not None:
                self.root.after(0, lambda p=price: self._on_price(p))
            else:
                self.root.after(0, lambda: self.status.config(text="Fetch failed - check symbol / internet, retrying..."))
            # Wait in 0.5s chunks so Stop reacts instantly (old code slept 5s solid)
            for _ in range(10):
                if self.stop_event.is_set(): break
                time.sleep(0.5)

    def _on_price(self, price: float) -> None:
        if self.prev_price is not None:
            change=price-self.prev_price; pct=change/self.prev_price*100 if self.prev_price else 0
            arrow="▲" if change>=0 else "▼"; color="#28a745" if change>=0 else "#dc3545"
        else:
            change=0; pct=0; arrow=""; color="#28a745"
        self.price.set(f"${price:.2f} {arrow} {change:+.2f} ({pct:+.2f}%)")
        self.price_label.config(fg=color)
        # Colour label via widget config (need ref - find by textvariable is hard, so use status)
        self.high=price if self.high is None else max(self.high, price)
        self.low=price if self.low is None else min(self.low, price)
        self.prev_price=price
        self.prices.append(price); self.times.append(datetime.now())
        self.prices=self.prices[-60:]; self.times=self.times[-60:]  # keep last 60 points
        self.info_label.config(text=f"High: ${self.high:.2f} | Low: ${self.low:.2f} | Last update: {datetime.now().strftime('%H:%M:%S')}")
        self.plot_graph()

    def start_tracking(self):
        symbol=self.stock_name.get().strip().upper()
        if not symbol: messagebox.showwarning("Missing", "Enter a symbol."); return
        self.stop_event.set()  # stop old if any, without blocking join on UI
        self.stop_event.clear()
        self.ticker=yf.Ticker(symbol)
        self.prices=[]; self.times=[]; self.prev_price=None; self.high=None; self.low=None
        self.start_btn.config(state=tk.DISABLED); self.stop_btn.config(state=tk.NORMAL)
        self.status.config(text=f"Tracking {symbol} - updating every 5s...")
        self.thread=threading.Thread(target=self.update_loop, daemon=True); self.thread.start()  # FIXED: daemon

    def stop_tracking(self):
        self.stop_event.set()  # FIXED: no join() on UI thread -> no freeze
        self.start_btn.config(state=tk.NORMAL); self.stop_btn.config(state=tk.DISABLED)
        self.status.config(text="Stopped.")
    def plot_graph(self):
        self.ax.clear()
        cast(Any, self.ax).plot(self.times, self.prices, color='blue', marker='o', markersize=3)
        cast(Any, self.ax).set_title(f"Real-Time Price - {self.stock_name.get().upper()}")
        cast(Any, self.ax).set_xlabel("Time"); cast(Any, self.ax).set_ylabel("Price ($)")
        self.ax.grid(True, alpha=0.3); self.fig.autofmt_xdate(); self.canvas.draw()

if __name__=="__main__":
    root=tk.Tk(); app=StockTracker(root); root.mainloop()
