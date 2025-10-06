import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message, from_addr, to_addr, password):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    
    body = message
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()

# Example usage:
if __name__ == "__main__":
    subject = "Let's Connect!"
    message = "Hi, I'd love to connect with you."
    from_addr = "your-email@gmail.com"
    password = "your-password"
    
    # List of recipient emails
    recipient_emails = ["recipient1@example.com", "recipient2@example.com"]
    
    for to_addr in recipient_emails:
        send_email(subject, message, from_addr, to_addr, password)
        print(f"Email sent to {to_addr}")