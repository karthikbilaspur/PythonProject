import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time

def send_email(to, name):
    # Email configuration
    from_email = "your-email@gmail.com"
    password = "your-password"
    subject = "Happy Birthday!"

    # Create a message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject

    # Email body
    body = f"Dear {name},\n\nHappy Birthday! Wishing you a wonderful day filled with love, laughter, and all your favorite things.\n\nBest regards,"
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to, text)
    server.quit()

def check_birthdays():
    # Load birthdays from a CSV file
    birthdays = pd.read_csv('birthdays.csv')

    # Get today's date
    today = datetime.date.today()

    # Check if today is someone's birthday
    for index, row in birthdays.iterrows():
        birthday = datetime.date(today.year, row['month'], row['day'])
        if today == birthday:
            send_email(row['email'], row['name'])
            print(f"Sent birthday wish to {row['name']}")

def main():
    while True:
        check_birthdays()
        time.sleep(86400)  # Check every day

if __name__ == "__main__":
    main()