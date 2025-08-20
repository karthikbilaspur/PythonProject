import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import ssl
from datetime import datetime

class EmailSender:
    def __init__(self, sender_email, sender_password, smtp_server, smtp_port):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, recipients, subject, body, attachment=None):
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Create a message
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = ', '.join(recipients)
        message['Subject'] = subject

        # Add the body to the message
        message.attach(MIMEText(body, 'plain'))

        # Add an attachment if specified
        if attachment:
            with open(attachment, 'rb') as f:
                attachment_data = f.read()
            attachment_mime = MIMEApplication(attachment_data)
            attachment_mime.add_header('Content-Disposition', f'attachment; filename= {attachment.split("/")[-1]}')
            message.attach(attachment_mime)

        # Send the email
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as smtp:
            smtp.login(self.sender_email, self.sender_password)
            smtp.sendmail(self.sender_email, recipients, message.as_string())

class EmailScheduler:
    def __init__(self, email_sender):
        self.email_sender = email_sender
        self.schedule = schedule

    def schedule_email(self, recipients, subject, body, attachment=None, schedule_time=None, interval=None):
        if schedule_time:
            self.schedule.every().day.at(schedule_time).do(self.email_sender.send_email, recipients, subject, body, attachment)
        elif interval:
            if interval == 'daily':
                self.schedule.every().day.do(self.email_sender.send_email, recipients, subject, body, attachment)
            elif interval == 'weekly':
                self.schedule.every().monday.do(self.email_sender.send_email, recipients, subject, body, attachment)
            elif interval == 'monthly':
                self.schedule.every(30).days.do(self.email_sender.send_email, recipients, subject, body, attachment)

    def run_schedule(self):
        while True:
            self.schedule.run_pending()
            time.sleep(1)

# Example usage
if __name__ == '__main__':
    sender_email = 'your-email@gmail.com'
    sender_password = 'your-password'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

    email_sender = EmailSender(sender_email, sender_password, smtp_server, smtp_port)
    email_scheduler = EmailScheduler(email_sender)

    recipients = ['recipient1@example.com', 'recipient2@example.com']
    subject = 'Test Email'
    body = 'This is a test email sent using Python.'
    attachment = 'path/to/attachment.pdf'

    # Schedule an email to be sent at a specific time
    schedule_time = '08:00'
    email_scheduler.schedule_email(recipients, subject, body, attachment, schedule_time=schedule_time)

    # Schedule an email to be sent at a specific interval
    interval = 'daily'
    email_scheduler.schedule_email(recipients, subject, body, attachment, interval=interval)

    email_scheduler.run_schedule()
    