import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StockTracker:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Real-Time Stock Tracker")
        self.stock_name = tk.StringVar()
        self.price = tk.StringVar(value="Fetching...")

        # Create input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10)

        tk.Label(input_frame, text="Stock Name:").grid(row=0, column=0)
        tk.Entry(input_frame, textvariable=self.stock_name).grid(row=0, column=1)

        # Create button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=10)

        tk.Button(button_frame, text="Start Tracking", command=self.start_tracking).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Stop Tracking", command=self.stop_tracking).pack(side=tk.LEFT, padx=10)

        # Create price label
        tk.Label(self.root, textvariable=self.price, font=("Arial", 24, "bold"), fg="#28a745").pack(pady=20)

        # Create graph frame
        graph_frame = tk.Frame(self.root)
        graph_frame.pack(padx=10, pady=10)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.stock_prices = []
        self.times = []
        self.stop_event = threading.Event()
        self.current_thread = None

    def fetch_stock_price(self):
        try:
            stock = yf.Ticker(self.stock_name.get())
            data = stock.history(period='1d', interval='1m')
            return data['Close'].iloc[-1]
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None

    def update_stock_price(self):
        while not self.stop_event.is_set():
            price = self.fetch_stock_price()
            if price:
                self.price.set(f"${price:.2f}")
                self.stock_prices.append(price)
                self.times.append(time.strftime("%H:%M:%S"))
                self.plot_graph()
            time.sleep(5)

    def start_tracking(self):
        if self.current_thread and self.current_thread.is_alive():
            self.stop_event.set()
            self.current_thread.join()

        self.stop_event.clear()
        self.current_thread = threading.Thread(target=self.update_stock_price)
        self.current_thread.start()

    def stop_tracking(self):
        self.stop_event.set()
        if self.current_thread:
            self.current_thread.join()

    def plot_graph(self):
        self.ax.clear()
        self.ax.plot(self.times, self.stock_prices, color='blue')
        self.ax.set_title(f"Real-Time Stock Price Graph ({self.stock_name.get()})")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price ($)")
        self.ax.grid()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = StockTracker(root)
    root.mainloop()