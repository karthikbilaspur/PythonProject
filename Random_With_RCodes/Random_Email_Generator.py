import random
import string
import csv
from tkinter import *
from tkinter import filedialog, messagebox
from threading import Thread
import progressbar

class EmailGenerator:
    def __init__(self):
        self.root = Tk()
        self.root.title("Email Generator")
        self.format = StringVar()
        self.format.set("random")

        self.count_label = Label(self.root, text="Enter count:")
        self.count_label.pack()
        self.count_entry = Entry(self.root)
        self.count_entry.pack()

        self.format_label = Label(self.root, text="Choose format:")
        self.format_label.pack()
        self.format_frame = Frame(self.root)
        self.format_frame.pack()
        self.random_format = Radiobutton(self.format_frame, text="Random", variable=self.format, value="random")
        self.random_format.pack(side=LEFT)
        self.first_last_format = Radiobutton(self.format_frame, text="First.Last", variable=self.format, value="first.last")
        self.first_last_format.pack(side=LEFT)
        self.initial_last_format = Radiobutton(self.format_frame, text="Initial.Last", variable=self.format, value="initial.last")
        self.initial_last_format.pack(side=LEFT)

        self.generate_button = Button(self.root, text="Generate", command=self.generate_emails)
        self.generate_button.pack()

        self.save_button = Button(self.root, text="Save to CSV", command=self.save_to_csv)
        self.save_button.pack()

        self.print_button = Button(self.root, text="Print Emails", command=self.print_emails)
        self.print_button.pack()

        self.status_label = Label(self.root, text="")
        self.status_label.pack()

        self.emails = []

    def make_email(self, format: str) -> str:
        extensions = ['com', 'net', 'org', 'gov']
        domains = [
            'gmail', 'yahoo', 'comcast', 'verizon', 'charter', 'hotmail',
            'outlook', 'frontier'
        ]

        finalext = random.choice(extensions)
        finaldom = random.choice(domains)
        accountlen = random.randint(1, 20)
        finalacc = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(accountlen))

        if format == "first.last":
            first_name = random.choice(["john", "jane", "mike", "sarah", "david"])
            last_name = random.choice(["smith", "johnson", "williams", "jones", "brown"])
            return f"{first_name}.{last_name}@{finaldom}.{finalext}"
        elif format == "initial.last":
            first_initial = random.choice(string.ascii_lowercase)
            last_name = random.choice(["smith", "johnson", "williams", "jones", "brown"])
            return f"{first_initial}.{last_name}@{finaldom}.{finalext}"
        elif format == "random":
            return f"{finalacc}@{finaldom}.{finalext}"
        else:
            raise ValueError("Invalid format")

    def generate_emails(self):
        try:
            count = int(self.count_entry.get())
            if count <= 0:
                messagebox.showerror("Error", "Count must be a positive integer.")
                return
        except ValueError:
            messagebox.showerror("Error", "Count must be an integer.")
            return

        self.status_label.config(text="Generating emails...")
        self.generate_button.config(state=DISABLED)

        def generate():
            self.emails = []
            bar = progressbar.ProgressBar(maxval=count)
            for i in bar(range(count)):
                while True:
                    email = self.make_email(self.format.get())
                    if email not in self.emails:
                        self.emails.append(email)
                        break
                bar.update(i + 1)
            self.status_label.config(text="Emails generated.")
            self.generate_button.config(state=NORMAL)

        thread = Thread(target=generate)
        thread.start()

    def save_to_csv(self):
        if not self.emails:
            messagebox.showerror("Error", "No emails generated.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filename:
            return

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Email"])
            for email in self.emails:
                writer.writerow([email])

        messagebox.showinfo("Success", "Emails saved to CSV file.")

    def print_emails(self):
        if not self.emails:
            messagebox.showerror("Error", "No emails generated.")
            return

        email_window = Toplevel(self.root)
        email_window.title("Emails")
        email_text = Text(email_window)
        email_text.pack(fill=BOTH, expand=True)
        for email in self.emails:
            email_text.insert(END, email + "\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    generator = EmailGenerator()
    generator.run()