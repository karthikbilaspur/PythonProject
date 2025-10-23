from tkinter import *
from tkinter import messagebox
import os
import pyqrcode
import smtplib
import imghdr
from email.message import EmailMessage

my_mail = "ENTER YOUR EMAIL ID"
password = "SET PASSWORD"

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator APP")
        self.create_widgets()

    def create_widgets(self):
        self.subject_label = Label(self.root, text="Enter URL/Subject")
        self.subject_label.grid(row=0, column=0, sticky=N + S + W + E)

        self.subject_entry = Entry(self.root, width=40)
        self.subject_entry.grid(row=0, column=1, sticky=N + S + W + E)

        self.filename_label = Label(self.root, text="Enter filename to save as")
        self.filename_label.grid(row=1, column=0, sticky=N + S + W + E)

        self.filename_entry = Entry(self.root, width=40)
        self.filename_entry.grid(row=1, column=1, sticky=N + S + W + E)

        self.email_label = Label(self.root, text="Enter email address")
        self.email_label.grid(row=2, column=0, sticky=N + S + W + E)

        self.email_entry = Entry(self.root, width=40)
        self.email_entry.grid(row=2, column=1, sticky=N + S + W + E)

        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=0, column=3, rowspan=3, sticky=N + S + W + E)

        self.generate_button = Button(self.button_frame, text="Generate QR Code", width=15, command=self.generate_qr_code)
        self.generate_button.pack(pady=5)

        self.save_button = Button(self.button_frame, text="Save as PNG File", width=15, command=self.save_qr_code)
        self.save_button.pack(pady=5)

        self.send_button = Button(self.button_frame, text="Send QR code", width=15, command=self.send_qr_code)
        self.send_button.pack(pady=5)

        self.image_label = Label(self.root)
        self.image_label.grid(row=4, column=1, sticky=N + S + W + E)

        self.status_label = Label(self.root, text="")
        self.status_label.grid(row=3, column=1, sticky=N + S + W + E)

        for row in range(5):
            self.root.grid_rowconfigure(row, weight=1)

        for col in range(4):
            self.root.grid_columnconfigure(col, weight=1)

    def generate_qr_code(self):
        subject = self.subject_entry.get()
        if subject:
            qr = pyqrcode.create(subject)
            self.photo = BitmapImage(data=qr.xbm(scale=8))
            self.image_label.config(image=self.photo)
            self.status_label.config(text=f"QR of {subject}")
        else:
            messagebox.showerror("Error", "Enter subject first")

    def save_qr_code(self):
        filename = self.filename_entry.get()
        if filename:
            try:
                qr = pyqrcode.create(self.subject_entry.get())
                qr.png(f"{filename}.png", scale=8)
                messagebox.showinfo("Status", "QR code saved successfully")
            except:
                messagebox.showerror("Error", "Generate the QR code first")
        else:
            messagebox.showerror("Error", "Enter filename first")

    def send_qr_code(self):
        try:
            email = self.email_entry.get()
            filename = self.filename_entry.get()
            if email and filename:
                new_message = EmailMessage()
                new_message['Subject'] = "QR CODE IS READY!!"
                new_message['From'] = my_mail
                new_message['To'] = email
                with open(f'{filename}.png', 'rb') as f:
                    image_data = f.read()
                    image_type = imghdr.what(f.name)
                    image_name = f.name
                new_message.add_attachment(
                    image_data, maintype='image', subtype=image_type, filename=image_name)
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(my_mail, password)
                    smtp.send_message(new_message)

                messagebox.showinfo("Status", "Mail has been sent successfully")
            else:
                messagebox.showerror("Error", "Invalid Email or QR Code not generated")
        except:
            messagebox.showerror("Error", "Invalid Email")


if __name__ == "__main__":
    root = Tk()
    app = QRCodeGenerator(root)
    root.mainloop()