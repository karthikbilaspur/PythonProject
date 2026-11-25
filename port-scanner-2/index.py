"""
Port Scanner - Medium Level
Features: threaded scan (no UI freeze), hostname validation, port range validation,
common service names, progress bar, cancel, export to CSV/TXT, safe timeout.
Use ONLY on hosts you own or have permission to scan.
"""
import csv
import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",143:"IMAP",443:"HTTPS",3306:"MySQL",5432:"PostgreSQL",6379:"Redis",8080:"HTTP-Alt",27017:"MongoDB"}

class PortScanner:
    def __init__(self, root):
        self.root = root; self.root.title("Port Scanner - Use only on your own hosts"); self.root.geometry("560x520")
        self.stop_flag = threading.Event(); self.results = []
        frm = ttk.Frame(root, padding=12); frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Host:").grid(row=0, column=0, sticky="w")
        self.host = ttk.Entry(frm, width=35); self.host.insert(0, "127.0.0.1"); self.host.grid(row=0, column=1, padx=5, pady=4)
        ttk.Label(frm, text="Start Port:").grid(row=1, column=0, sticky="w")
        self.start = ttk.Entry(frm, width=10); self.start.insert(0, "1"); self.start.grid(row=1, column=1, sticky="w", padx=5, pady=4)
        ttk.Label(frm, text="End Port:").grid(row=2, column=0, sticky="w")
        self.end = ttk.Entry(frm, width=10); self.end.insert(0, "1024"); self.end.grid(row=2, column=1, sticky="w", padx=5, pady=4)
        ttk.Label(frm, text="Timeout (s):").grid(row=3, column=0, sticky="w")
        self.timeout = ttk.Entry(frm, width=10); self.timeout.insert(0, "0.5"); self.timeout.grid(row=3, column=1, sticky="w", padx=5, pady=4)
        ttk.Label(frm, text="Threads:").grid(row=4, column=0, sticky="w")
        self.threads = ttk.Entry(frm, width=10); self.threads.insert(0, "50"); self.threads.grid(row=4, column=1, sticky="w", padx=5, pady=4)
        btns = ttk.Frame(frm); btns.grid(row=5, column=0, columnspan=2, pady=8)
        self.scan_btn = ttk.Button(btns, text="Scan", command=self.start_scan); self.scan_btn.pack(side="left", padx=4)
        self.stop_btn = ttk.Button(btns, text="Stop", command=self.stop_scan, state="disabled"); self.stop_btn.pack(side="left", padx=4)
        ttk.Button(btns, text="Export CSV", command=self.export).pack(side="left", padx=4)
        ttk.Button(btns, text="Clear", command=self.clear).pack(side="left", padx=4)
        self.progress = ttk.Progressbar(frm, mode="determinate"); self.progress.pack(fill="x", pady=5)
        self.status = ttk.Label(frm, text="Ready"); self.status.pack()
        self.text = tk.Text(frm, height=18); self.text.pack(fill="both", expand=True, pady=5)

    def validate(self):
        host = self.host.get().strip()
        if not host: raise ValueError("Host is required")
        try: socket.gethostbyname(host)
        except socket.gaierror: raise ValueError(f"Cannot resolve host: {host}")
        try:
            s, e = int(self.start.get()), int(self.end.get())
            t = float(self.timeout.get()); th = int(self.threads.get())
        except ValueError: raise ValueError("Ports / timeout / threads must be numbers")
        if not (1 <= s <= 65535 and 1 <= e <= 65535): raise ValueError("Ports must be 1-65535")
        if s > e: raise ValueError("Start port must be <= end port")
        if e - s > 10000: raise ValueError("Max 10,000 ports per scan for safety")
        if not (0.1 <= t <= 5): raise ValueError("Timeout must be 0.1 - 5s")
        if not (1 <= th <= 200): raise ValueError("Threads must be 1-200")
        return host, s, e, t, th

    def check_port(self, host, port, timeout):
        if self.stop_flag.is_set(): return None
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                if sock.connect_ex((host, port)) == 0:
                    try: service = socket.getservbyport(port)
                    except OSError: service = COMMON_PORTS.get(port, "unknown")
                    return (port, service)
        except OSError: return None
        return None

    def start_scan(self):
        try: host, s, e, t, th = self.validate()
        except ValueError as ex: messagebox.showerror("Invalid input", str(ex)); return
        self.clear(); self.stop_flag.clear(); self.results = []
        self.scan_btn.config(state="disabled"); self.stop_btn.config(state="normal")
        self.progress["maximum"] = e - s + 1; self.progress["value"] = 0
        threading.Thread(target=self._run, args=(host, s, e, t, th), daemon=True).start()

    def _run(self, host, s, e, t, th):
        done = 0
        with ThreadPoolExecutor(max_workers=th) as ex:
            futures = {ex.submit(self.check_port, host, p, t): p for p in range(s, e+1)}
            for fut in futures:
                if self.stop_flag.is_set(): break
                res = fut.result()
                done += 1
                self.root.after(0, lambda d=done: self.progress.config(value=d))
                if res:
                    self.results.append(res)
                    svc = res[1]
                    self.root.after(0, lambda r=res: self.text.insert("end", f"Port {r[0]} OPEN ({r[1]})\n"))
                self.root.after(0, lambda: self.status.config(text=f"Scanned {done}/{e-s+1} • Open: {len(self.results)}"))
        self.root.after(0, self._finish)

    def _finish(self):
        self.scan_btn.config(state="normal"); self.stop_btn.config(state="disabled")
        self.status.config(text=f"Done. {len(self.results)} open port(s) found.")
        if not self.results: self.text.insert("end", "No open ports found in range.\n")

    def stop_scan(self): self.stop_flag.set(); self.status.config(text="Stopping...")
    def clear(self): self.text.delete("1.0", "end"); self.results = []; self.progress["value"] = 0; self.status.config(text="Ready")
    def export(self):
        if not self.results: messagebox.showinfo("Export", "No results to export."); return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path: return
        with open(path, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["port","service"]); w.writerows(sorted(self.results))
        messagebox.showinfo("Export", f"Saved to {path}")

if __name__ == "__main__":
    root = tk.Tk(); PortScanner(root); root.mainloop()
