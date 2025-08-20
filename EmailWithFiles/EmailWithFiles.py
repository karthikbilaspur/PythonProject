import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

class EmailSender:
    def __init__(self, sender_email, sender_password, smtp_server, smtp_port):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email_with_file(self, receiver_email, subject, body, files=[]):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = receiver_email
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(body))

        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(path).name))
            msg.attach(part)

        smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        smtp.starttls()
        smtp.login(self.sender_email, self.sender_password)
        smtp.sendmail(self.sender_email, receiver_email, msg.as_string())
        smtp.quit()

# Example usage
if __name__ == '__main__':
    sender_email = 'your-email@gmail.com'
    sender_password = 'your-password'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    receiver_email = 'receiver-email@example.com'
    subject = 'Test Email with File'
    body = 'This is a test email with a file attachment.'
    files = ['path/to/file.pdf']

    email_sender = EmailSender(sender_email, sender_password, smtp_server, smtp_port)
    email_sender.send_email_with_file(receiver_email, subject, body, files)