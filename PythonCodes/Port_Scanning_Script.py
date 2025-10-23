import tkinter as tk
from tkinter import messagebox
import socket

class PortScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Port Scanner")
        self.host_label = tk.Label(self.root, text="Host:")
        self.host_label.pack()
        self.host_entry = tk.Entry(self.root)
        self.host_entry.pack()
        self.start_port_label = tk.Label(self.root, text="Start Port:")
        self.start_port_label.pack()
        self.start_port_entry = tk.Entry(self.root)
        self.start_port_entry.pack()
        self.end_port_label = tk.Label(self.root, text="End Port:")
        self.end_port_label.pack()
        self.end_port_entry = tk.Entry(self.root)
        self.end_port_entry.pack()
        self.scan_button = tk.Button(self.root, text="Scan", command=self.scan_ports)
        self.scan_button.pack()
        self.result_text = tk.Text(self.root)
        self.result_text.pack()

    def scan_ports(self):
        host = self.host_entry.get()
        start_port = int(self.start_port_entry.get())
        end_port = int(self.end_port_entry.get())
        self.result_text.delete(1.0, tk.END)
        for port in range(start_port, end_port + 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    self.result_text.insert(tk.END, f"Port {port} is open\n")
                sock.close()
            except socket.error:
                self.result_text.insert(tk.END, f"Error scanning port {port}\n")
        messagebox.showinfo("Scan Complete", "Port scan complete.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    scanner = PortScanner()
    scanner.run()