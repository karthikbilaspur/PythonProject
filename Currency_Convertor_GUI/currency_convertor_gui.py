import tkinter as tk
from tkinter import messagebox
import requests

class CurrencyConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Currency Converter")

        # API endpoint and API key
        self.api_endpoint = "https://api.exchangerate-api.com/v4/latest/"
        self.api_key = ""  # Not required for this API

        # GUI components
        self.amount_label = tk.Label(self.window, text="Amount:")
        self.amount_label.grid(row=0, column=0)

        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.grid(row=0, column=1)

        self.from_currency_label = tk.Label(self.window, text="From:")
        self.from_currency_label.grid(row=1, column=0)

        self.from_currency_var = tk.StringVar(self.window)
        self.from_currency_var.set("USD")
        self.from_currency_option = tk.OptionMenu(self.window, self.from_currency_var, "USD", "EUR", "GBP", "INR", "AUD")
        self.from_currency_option.grid(row=1, column=1)

        self.to_currency_label = tk.Label(self.window, text="To:")
        self.to_currency_label.grid(row=2, column=0)

        self.to_currency_var = tk.StringVar(self.window)
        self.to_currency_var.set("EUR")
        self.to_currency_option = tk.OptionMenu(self.window, self.to_currency_var, "USD", "EUR", "GBP", "INR", "AUD")
        self.to_currency_option.grid(row=2, column=1)

        self.convert_button = tk.Button(self.window, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=3, column=0)

        self.clear_button = tk.Button(self.window, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=3, column=1)

        self.history_button = tk.Button(self.window, text="History", command=self.show_history)
        self.history_button.grid(row=4, column=0, columnspan=2)

        self.result_label = tk.Label(self.window, text="")
        self.result_label.grid(row=5, column=0, columnspan=2)

        self.history = []

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency_var.get()
            to_currency = self.to_currency_var.get()

            response = requests.get(self.api_endpoint + from_currency)
            data = response.json()

            if "rates" in data and to_currency in data["rates"]:
                rate = data["rates"][to_currency]
                result = amount * rate
                self.result_label.config(text=f"{amount} {from_currency} = {result} {to_currency}")
                self.history.append(f"{amount} {from_currency} = {result} {to_currency}")
            else:
                messagebox.showerror("Error", "Invalid currency or API response")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def clear_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.result_label.config(text="")

    def show_history(self):
        history_window = tk.Toplevel(self.window)
        history_window.title("Conversion History")

        history_text = tk.Text(history_window)
        history_text.pack()

        for conversion in self.history:
            history_text.insert(tk.END, conversion + "\n")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    converter = CurrencyConverter()
    converter.run()