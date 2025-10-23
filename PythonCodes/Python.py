import tkinter as tk
from tkinter import messagebox
import requests
import hashlib

class PwnedPasswordChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pwned or Not?")
        self.root.geometry("400x150")

        self.pass_var = tk.StringVar()
        self.password_entry = tk.Entry(self.root, textvariable=self.pass_var, font=('Ubuntu', 12, 'bold'), show='*', justify='center')
        self.password_entry.place(x=100, y=25)

        self.pass_label = tk.Label(self.root, text='Enter your password:', font=('Ubuntu', 12, 'bold'))
        self.pass_label.place(x=100)

        self.show_button = tk.Button(self.root, text="Show", command=self.show_password)
        self.show_button.place(x=115, y=55)

        self.hide_button = tk.Button(self.root, text="Hide", command=self.hide_password)
        self.hide_button.place(x=235, y=55)

        self.sub_btn = tk.Button(self.root, text='Submit', font=('Ubuntu', 12, 'bold'), command=self.check_password)
        self.sub_btn.place(x=160, y=100)

    def show_password(self):
        self.password_entry.config(show='')

    def hide_password(self):
        self.password_entry.config(show='*')

    def password_hashing(self, password: str):
        sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        return sha1pass[:5], sha1pass[5:]

    def send_request_to_API(self, start_char: str):
        url = f'https://api.pwnedpasswords.com/range/{start_char}'
        try:
            res = requests.get(url)
            if res.status_code != 200:
                messagebox.showerror("Error", "Failed to fetch results")
                return None
            return res
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", "Connection Error")
            return None

    def get_count(self, res: requests.Response, suffix: str) -> int:
        results = (line.split(':') for line in res.text.splitlines())
        for hashed, count in results:
            if hashed == suffix:
                return count
        return 0

    def check_password(self):
        password = self.pass_var.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return

        start, end = self.password_hashing(password)
        res = self.send_request_to_API(start)
        if res:
            num = self.get_count(res, end)
            if num:
                messagebox.showwarning("Warning", f'Password found {num} times in the dataset. Recommended to change it ASAP!')
            else:
                messagebox.showinfo("Info", 'Your password was not found in the dataset. You have a safe password!')

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = PwnedPasswordChecker()
    app.run()