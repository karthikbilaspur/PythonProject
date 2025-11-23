import tkinter as tk
from tkinter import messagebox
import requests

class WebsiteStatusChecker:
    def __init__(self:'WebsiteStatusChecker') -> None:
        self.window = tk.Tk()
        self.window.title("Website Status Checker")

        # Create input field for website URL
        self.url_label = tk.Label(self.window, text="Enter Website URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.window, width=50)
        self.url_entry.pack()

        # Create button to check website status
        self.check_button = tk.Button(self.window, text="Check Status", command=self.check_status)
        self.check_button.pack()

        # Create label to display website status
        self.status_label = tk.Label(self.window, text="")
        self.status_label.pack()

    def check_status(self):
        url = self.url_entry.get()
        try:
            response = requests.head(url)
            status_code = response.status_code
            if status_code = status_code
        except requests.RequestException as e:
            status_code = str(e)

        if status_code == 200:
            self.status_label.config(text="Website is up and running", fg="green")
        else:
            self.status_label.config(text=f"Website is down. Status code: {status_code}", fg="red")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = WebsiteStatusChecker()
    app.run()