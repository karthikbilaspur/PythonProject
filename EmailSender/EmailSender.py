

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import ssl

class EmailSender:
    def __init__(self, sender_email, sender_password, smtp_server, smtp_port):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, recipients, subject, body, attachment=None, cc=None, bcc=None):
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Create a message
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = ', '.join(recipients)
        message['Subject'] = subject

        if cc:
            message['Cc'] = ', '.join(cc)
        if bcc:
            message['Bcc'] = ', '.join(bcc)

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
            smtp.sendmail(self.sender_email, recipients + (cc or []) + (bcc or []), message.as_string())

    def send_html_email(self, recipients, subject, html_body, attachment=None, cc=None, bcc=None):
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Create a message
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = ', '.join(recipients)
        message['Subject'] = subject

        if cc:
            message['Cc'] = ', '.join(cc)
        if bcc:
            message['Bcc'] = ', '.join(bcc)

        # Add the HTML body to the message
        message.attach(MIMEText(html_body, 'html'))

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
            smtp.sendmail(self.sender_email, recipients + (cc or []) + (bcc or []), message.as_string())

# Example usage
if __name__ == '__main__':
    sender_email = 'your-email@gmail.com'
    sender_password = 'your-password'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

    email_sender = EmailSender(sender_email, sender_password, smtp_server, smtp_port)

    recipients = ['recipient1@example.com', 'recipient2@example.com']
    subject = 'Test Email'
    body = 'This is a test email sent using Python.'

    email_sender.send_email(recipients, subject, body)

    html_body = '<html><body><h1>This is a test HTML email sent using Python.</h1></body></html>'
    email_sender.send_html_email(recipients, subject, html_body)

    attachment = 'path/to/attachment.pdf'
    email_sender.send_email(recipients, subject, body, attachment)

    cc = ['cc-recipient@example.com']
    bcc = ['bcc-recipient@example.com']
    email_sender.send_email(recipients, subject, body, cc=cc, bcc=bcc)