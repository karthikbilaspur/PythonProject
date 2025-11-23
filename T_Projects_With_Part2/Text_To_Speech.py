import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from tkinter import messagebox

class TextToSheets:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', self.scope{)})
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.client.open('Sheet Name').sheet1

    def write_to_sheet(self, text: str):
        try:
            self.sheet.append_row([text])
            messagebox.showinfo("Success", "Text written to sheet successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_from_sheet(self):
        try:
            data = self.sheet.get_all_records(())
            return data
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_sheet(self):
        try:
            self.sheet.clear()
            messagebox.showinfo("Success", "Sheet cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    root.title("Text to Sheets")

    text_to_sheets = TextToSheets()

    tk.Label(root, text="Enter text:").pack()
    text_entry = tk.Entry(root, width=50)
    text_entry.pack()

    def write_text():
        text = text_entry.get()
        if text:
            text_to_sheets.write_to_sheet(text)
        else:
            messagebox.showerror("Error", "Please enter text!")

    tk.Button(root, text="Write to Sheet", command=write_text).pack()

    def read_text():
        data = text_to_sheets.read_from_sheet()
        if data:
            read_window = tk.Toplevel(root)
            read_window.title("Sheet Data")
            tk.Label(read_window, text=str(data)).pack()
        else:
            messagebox.showerror("Error", "No data in sheet!")

    tk.Button(root, text="Read from Sheet", command=read_text).pack()

    def clear_text():
        clear_window = tk.Toplevel(root)
        clear_window.title("Clear Sheet")
        tk.Label(clear_window, text="Are you sure you want to clear the sheet?").pack()
        tk.Button(clear_window, text="Yes", command=text_to_sheets.clear_sheet).pack()
        tk.Button(clear_window, text="No", command=clear_window.destroy).pack()

    tk.Button(root, text="Clear Sheet", command=clear_text).pack()

    root.mainloop()

if __name__ == "__main__":
    main()