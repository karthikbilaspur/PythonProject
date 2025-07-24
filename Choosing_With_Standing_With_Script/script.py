import schedule
import time
import os
import shutil
import requests
from bs4 import
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define constants
SOURCE_DIR = '/path/to/source'
DESTINATION_DIR = '/path/to/destination'
URL = 'http://example.com'
FROM_EMAIL = 'your-email@gmail.com'
TO_EMAIL = 'recipient-email@gmail.com'
PASSWORD = 'your-password'

# Function to move files
def move_files():
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".txt"):
            shutil.move(os.path.join(SOURCE_DIR, filename), DESTINATION_DIR)
    print("Files moved successfully")

# Function to scrape website
def scrape_website():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    return links

# Function to send email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM_EMAIL, PASSWORD)
    server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    server.quit()
    print("Email sent successfully")

# Function to perform daily tasks
def daily_tasks():
    move_files()
    links = scrape_website()
    body = "Links scraped from {}: {}".format(URL, links)
    send_email("Daily Update", body)

# Schedule daily tasks
schedule.every().day.at("08:00").do(daily_tasks)  # Run daily tasks at 8am every day

# Run scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)