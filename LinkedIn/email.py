import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import time
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def send_emails(subject, message, from_addr, recipient_emails, password):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_addr, password)
        
        for to_addr in recipient_emails:
            if not validate_email_address(to_addr):
                print(f"Invalid email address: {to_addr}")
                continue
            
            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = to_addr
            msg['Subject'] = subject
            
            body = message
            msg.attach(MIMEText(body, 'plain'))
            
            text = msg.as_string()
            server.sendmail(from_addr, to_addr, text)
            print(f"Email sent to {to_addr}")
            time.sleep(1)  # Add a 1-second delay between emails
    except smtplib.SMTPAuthenticationError:
        print("Invalid email credentials")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
    finally:
        try:
            server.quit()
        except:
            pass

def main():
    subject = "Let's Connect!"
    message = "Hi, I'd love to connect with you."
    from_addr = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('EMAIL_PASSWORD')
    
    recipient_emails = ["recipient1@example.com", "recipient2@example.com"]
    
    send_emails(subject, message, from_addr, recipient_emails, password)

if __name__ == "__main__":
    main()