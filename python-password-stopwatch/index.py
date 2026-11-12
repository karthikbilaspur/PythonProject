import tkinter as tk
from tkinter import messagebox
import secrets
import string
import time


class PasswordGeneratorFrame(tk.LabelFrame):
    def __init__(self, master: tk.Misc):
        super().__init__(master, text="  Password Generator  ", padx=15, pady=15, font=("Helvetica", 11, "bold"))
        self.length_var = tk.StringVar(value="16")
        self.complexity = tk.StringVar(value="Complex")
        self.strength_var = tk.StringVar(value="Strength: -")
        self.build()

    def build(self):
        # Length
        row1 = tk.Frame(self)
        row1.pack(fill="x", pady=(0, 8))
        tk.Label(row1, text="Password Length:", font=("Helvetica", 10)).pack(side="left")
        tk.Entry(row1, textvariable=self.length_var, width=8, font=("Helvetica", 10)).pack(side="left", padx=(8, 0))

        # Complexity
        tk.Label(self, text="Complexity:", font=("Helvetica", 10, "bold")).pack(anchor="w")
        for text, value in [
            ("Simple  (a-z)", "Simple"),
            ("Medium  (a-z, A-Z)", "Medium"),
            ("Complex  (a-z, A-Z, 0-9, !@#$%^&*)", "Complex"),
        ]:
            tk.Radiobutton(self, text=text, variable=self.complexity, value=value, font=("Helvetica", 10)).pack(anchor="w")

        # Buttons
        btn_row = tk.Frame(self)
        btn_row.pack(fill="x", pady=(12, 8))
        tk.Button(btn_row, text="Generate Password", command=self.generate_password,
                  bg="#2563eb", fg="white", font=("Helvetica", 10, "bold"), padx=12, pady=6).pack(side="left")
        tk.Button(btn_row, text="Copy", command=self.copy_password,
                  font=("Helvetica", 10), padx=12, pady=6).pack(side="left", padx=(8, 0))

        # Output
        self.password_entry = tk.Entry(self, font=("Consolas", 12), width=42)
        self.password_entry.pack(fill="x", pady=(0, 6))
        tk.Label(self, textvariable=self.strength_var, font=("Helvetica", 10, "bold"), fg="#059669").pack(anchor="w")

    def generate_password(self):
        try:
            length = int(self.length_var.get())
            if length <= 0:
                raise ValueError
            if length > 128:
                messagebox.showwarning("Too long", "Keep length between 1 and 128")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid password length (1-128)")
            return

        complexity = self.complexity.get()
        if complexity == "Simple":
            characters = string.ascii_lowercase
        elif complexity == "Medium":
            characters = string.ascii_letters
        else:
            characters = string.ascii_letters + string.digits + "!@#$%^&*"

        # secrets is cryptographically secure - better than random for passwords
        password = ''.join(secrets.choice(characters) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.update_strength(password, complexity)

    def update_strength(self, password: str, complexity: str):
        score = len(password)
        if complexity == "Medium":
            score += 10
        elif complexity == "Complex":
            score += 20
        if score < 12:
            label, color = "Weak", "#dc2626"
        elif score < 22:
            label, color = "Medium", "#d97706"
        elif score < 32:
            label, color = "Strong", "#059669"
        else:
            label, color = "Very Strong", "#059669"
        self.strength_var.set(f"Strength: {label}  ({len(password)} chars)")
        # recolor label
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("textvariable") == str(self.strength_var):
                widget.config(fg=color)

    def copy_password(self):
        pwd = self.password_entry.get()
        if not pwd:
            messagebox.showinfo("Copy", "Generate a password first!")
            return
        self.clipboard_clear()
        self.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")


class StopwatchFrame(tk.LabelFrame):
    def __init__(self, master: tk.Misc):
        super().__init__(master, text="  Stopwatch  ", padx=15, pady=15, font=("Helvetica", 11, "bold"))
        self.running = False
        self.start_time = 0
        self.elapsed_before = 0
        self.laps: list[float] = []
        self.build()
        self.update_timer()

    def build(self):
        self.time_label = tk.Label(self, text="00:00:00.00", font=("Helvetica", 28, "bold"))
        self.time_label.pack(pady=(0, 10))

        btn_row = tk.Frame(self)
        btn_row.pack()
        self.start_button = tk.Button(btn_row, text="Start", command=self.start, bg="#16a34a", fg="white",
                                      font=("Helvetica", 10, "bold"), width=10, pady=5)
        self.start_button.pack(side="left", padx=3)
        self.stop_button = tk.Button(btn_row, text="Stop", command=self.stop, state="disabled",
                                     font=("Helvetica", 10, "bold"), width=10, pady=5)
        self.stop_button.pack(side="left", padx=3)
        tk.Button(btn_row, text="Lap", command=self.add_lap, font=("Helvetica", 10, "bold"), width=10, pady=5).pack(side="left", padx=3)
        tk.Button(btn_row, text="Reset", command=self.reset, font=("Helvetica", 10, "bold"), width=10, pady=5).pack(side="left", padx=3)

        # Lap list
        tk.Label(self, text="Laps:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(12, 4))
        self.lap_list = tk.Listbox(self, height=5, font=("Consolas", 10))
        self.lap_list.pack(fill="x")

    def format_time(self, total_seconds: float) -> str:
        hours, rem = divmod(total_seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        centiseconds = int((total_seconds - int(total_seconds)) * 100)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{centiseconds:02}"

    def current_elapsed(self):
        if self.running:
            return self.elapsed_before + (time.time() - self.start_time)
        return self.elapsed_before

    def update_timer(self):
        self.time_label.config(text=self.format_time(self.current_elapsed()))
        self.after(10, self.update_timer)

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")

    def stop(self):
        if self.running:
            self.elapsed_before = self.current_elapsed()
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def reset(self):
        self.running = False
        self.elapsed_before = 0
        self.start_time = 0
        self.laps.clear()
        self.lap_list.delete(0, tk.END)
        self.time_label.config(text="00:00:00.00")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def add_lap(self):
        elapsed = self.current_elapsed()
        self.laps.append(elapsed)
        self.lap_list.insert(tk.END, f"Lap {len(self.laps):02}  -  {self.format_time(elapsed)}")
        self.lap_list.see(tk.END)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator + Stopwatch")
        self.geometry("480x720")
        self.resizable(False, False)
        container = tk.Frame(self, padx=12, pady=12)
        container.pack(fill="both", expand=True)
        PasswordGeneratorFrame(container).pack(fill="x", pady=(0, 12))
        StopwatchFrame(container).pack(fill="x")


if __name__ == "__main__":
    app = App()
    app.mainloop()