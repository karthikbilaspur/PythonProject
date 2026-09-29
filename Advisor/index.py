import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import datetime
from pathlib import Path

class RandomAdvisorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Random Advisor - Wisdom on Demand")
        self.root.geometry("550x500")
        self.root.minsize(500, 450)
        self.root.configure(bg="#f5f7fb")
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=8)
        self.style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'), background="#f5f7fb", foreground="#2d3436")
        self.style.configure('Advice.TLabel', font=('Segoe UI', 13), background="white", foreground="#2d3436")
        
        self.advice_var = tk.StringVar(value="Loading wisdom...")
        self.status_var = tk.StringVar(value="Powered by adviceslip.com")
        self.advice_history: list[dict] = []
        self.history_file = Path("advice_history.json")
        
        self.load_history()
        self.create_widgets()
        self.fetch_advice()

    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#f5f7fb", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(main_frame, text="💡 Random Advisor", style='Title.TLabel')
        title.pack(pady=(0, 20))

        # Advice Card
        card = tk.Frame(main_frame, bg="white", relief=tk.FLAT, bd=0, highlightbackground="#dfe6e9", highlightthickness=1)
        card.pack(fill=tk.X, pady=10, ipady=20, ipadx=15)
        
        # Wrap length dynamic
        self.advice_label = tk.Label(
            card, 
            textvariable=self.advice_var,
            wraplength=450,
            font=("Segoe UI", 13),
            bg="white",
            fg="#2d3436",
            justify=tk.CENTER
        )
        self.advice_label.pack(pady=10, padx=10, fill=tk.X)

        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg="#f5f7fb")
        btn_frame.pack(pady=15)

        self.get_btn = ttk.Button(btn_frame, text="✨ Get New Advice", command=self.fetch_advice)
        self.get_btn.grid(row=0, column=0, padx=5)

        copy_btn = ttk.Button(btn_frame, text="📋 Copy", command=self.copy_advice)
        copy_btn.grid(row=0, column=1, padx=5)

        hist_btn = ttk.Button(btn_frame, text="📜 History", command=self.display_history)
        hist_btn.grid(row=0, column=2, padx=5)

        # Bottom actions
        bottom_frame = tk.Frame(main_frame, bg="#f5f7fb")
        bottom_frame.pack(fill=tk.X, pady=10)

        ttk.Button(bottom_frame, text="💾 Export History", command=self.export_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="🗑️ Clear History", command=self.clear_history).pack(side=tk.LEFT, padx=5)

        # Status / Footer
        footer = tk.Frame(self.root, bg="#dfe6e9", height=30)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, textvariable=self.status_var, font=("Segoe UI", 9), bg="#dfe6e9", fg="#636e72").pack(pady=5)

    def fetch_advice(self):
        self.advice_var.set("⏳ Fetching wisdom...")
        self.get_btn.config(state=tk.DISABLED)
        self.root.update_idletasks()
        try:
            # Cache buster
            res = requests.get("https://api.adviceslip.com/advice", timeout=8, headers={'Cache-Control': 'no-cache'})
            res.raise_for_status()
            data = res.json()
            advice = data.get("slip", {}).get("advice", "No advice found.")
            self.advice_var.set(f'"{advice}"')
            self.save_to_history(advice)
            self.status_var.set(f"Last updated: {datetime.datetime.now().strftime('%I:%M:%S %p')}")
        except requests.exceptions.Timeout:
            messagebox.showwarning("Timeout", "API is slow. Showing last advice from history if available.")
            if self.advice_history:
                self.advice_var.set(f'"{self.advice_history[-1]["advice"]}"')
            else:
                self.advice_var.set("⚠️ Could not connect. Please check your internet.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch advice:\n{str(e)}")
            self.advice_var.set("Failed to fetch. Click 'Get New Advice' to retry.")
        finally:
            self.get_btn.config(state=tk.NORMAL)

    def save_to_history(self, advice: str):
        entry = {
            "advice": advice,
            "timestamp": datetime.datetime.now().isoformat(),
            "date_str": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
        }
        # Avoid duplicates in a row
        if self.advice_history and self.advice_history[-1]["advice"] == advice:
            return
        self.advice_history.append(entry)
        if len(self.advice_history) > 50:  # keep 50
            self.advice_history.pop(0)
        self.save_history_to_file()

    def save_history_to_file(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.advice_history, f, indent=2, ensure_ascii=False)
        except: pass

    def load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.advice_history = json.load(f)
            except: self.advice_history = []

    def copy_advice(self):
        advice = self.advice_var.get().strip('"')
        self.root.clipboard_clear()
        self.root.clipboard_append(advice)
        self.status_var.set("✅ Copied to clipboard!")

    def display_history(self):
        if not self.advice_history:
            messagebox.showinfo("History", "No advice history yet. Fetch some wisdom first!")
            return

        win = tk.Toplevel(self.root)
        win.title("Advice History - Last 50")
        win.geometry("500x400")
        win.configure(bg="white")

        tk.Label(win, text=f"Total Advices: {len(self.advice_history)}", font=("Segoe UI", 11, "bold"), bg="white").pack(pady=10)

        text_frame = tk.Frame(win)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Segoe UI", 10), yscrollcommand=scrollbar.set, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        for i, entry in enumerate(reversed(self.advice_history), 1):
            text_widget.insert(tk.END, f"{i}. {entry['advice']}\n", "advice")
            text_widget.insert(tk.END, f"   — {entry['date_str']}\n\n", "date")

        text_widget.tag_config("advice", font=("Segoe UI", 10, "italic"))
        text_widget.tag_config("date", foreground="#636e72", font=("Segoe UI", 8))
        text_widget.config(state=tk.DISABLED)

    def export_history(self):
        if not self.advice_history:
            messagebox.showwarning("Export", "No history to export.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("Text", "*.txt")])
        if not file: return
        try:
            if file.endswith('.json'):
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump(self.advice_history, f, indent=2, ensure_ascii=False)
            else:
                with open(file, 'w', encoding='utf-8') as f:
                    for e in self.advice_history:
                        f.write(f"{e['date_str']} - {e['advice']}\n")
            messagebox.showinfo("Exported", f"History exported to {file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_history(self):
        if messagebox.askyesno("Clear", "Delete all advice history?"):
            self.advice_history.clear()
            self.save_history_to_file()
            self.status_var.set("History cleared")

def main():
    root = tk.Tk()
    app = RandomAdvisorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()