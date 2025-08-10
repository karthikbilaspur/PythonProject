import tkinter as tk
from tkinter import filedialog, messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv

class EmailSender:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk Email Sender")

        # Email configuration
        self.smtp_server_label = tk.Label(root, text="SMTP Server:")
        self.smtp_server_label.pack()
        self.smtp_server_entry = tk.Entry(root)
        self.smtp_server_entry.pack()

        self.smtp_port_label = tk.Label(root, text="SMTP Port:")
        self.smtp_port_label.pack()
        self.smtp_port_entry = tk.Entry(root)
        self.smtp_port_entry.pack()

        self.from_email_label = tk.Label(root, text="From Email:")
        self.from_email_label.pack()
        self.from_email_entry = tk.Entry(root)
        self.from_email_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # Email content
        self.subject_label = tk.Label(root, text="Subject:")
        self.subject_label.pack()
        self.subject_entry = tk.Entry(root)
        self.subject_entry.pack()

        self.body_label = tk.Label(root, text="Body:")
        self.body_label.pack()
        self.body_text = tk.Text(root, height=10, width=40)
        self.body_text.pack()

        # Recipient list
        self.recipient_list_label = tk.Label(root, text="Recipient List (CSV):")
        self.recipient_list_label.pack()
        self.recipient_list_entry = tk.Entry(root, width=50)
        self.recipient_list_entry.pack()
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        # Send email button
        self.send_button = tk.Button(root, text="Send Emails", command=self.send_emails)
        self.send_button.pack()

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.recipient_list_entry.delete(0, tk.END)
        self.recipient_list_entry.insert(0, filename)

    def send_emails(self):
        smtp_server = self.smtp_server_entry.get()
        smtp_port = int(self.smtp_port_entry.get())
        from_email = self.from_email_entry.get()
        password = self.password_entry.get()
        subject = self.subject_entry.get()
        body = self.body_text.get("1.0", tk.END)

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)

            with open(self.recipient_list_entry.get(), 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    to_email = row[0]
                    msg = MIMEMultipart()
                    msg['From'] = from_email
                    msg['To'] = to_email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    server.sendmail(from_email, to_email, msg.as_string())

            server.quit()
            messagebox.showinfo("Success", "Emails sent successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSender(root)
    root.mainloop()