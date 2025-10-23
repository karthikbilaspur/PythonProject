import tkinter as tk
from tkinter import messagebox
import requests

class PhoneNumberTracker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Phone Number Tracker")

        # Create input field for phone number
        self.phone_number_label = tk.Label(self.window, text="Enter Phone Number:")
        self.phone_number_label.pack()
        self.phone_number_entry = tk.Entry(self.window)
        self.phone_number_entry.pack()

        # Create button to track phone number
        self.track_button = tk.Button(self.window, text="Track", command=self.track_phone_number)
        self.track_button.pack()

        # Create text area to display result
        self.result_text = tk.Text(self.window, height=10, width=40)
        self.result_text.pack()

    def track_phone_number(self):
        phone_number = self.phone_number_entry.get()
        api_key = "YOUR_NUMVERIFY_API_KEY"  # Replace with your NumVerify API key

        try:
            response = requests.get(f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}")
            response.raise_for_status()
            data = response.json()

            if data['valid']:
                result = f"Phone Number: {data['international_format']}\n"
                result += f"Country: {data['country_name']}\n"
                result += f"Location: {data['location']}\n"
                result += f"Carrier: {data['carrier']}"
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert(tk.END, result)
            else:
                messagebox.showerror("Error", "Invalid phone number")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    tracker = PhoneNumberTracker()
    tracker.run()