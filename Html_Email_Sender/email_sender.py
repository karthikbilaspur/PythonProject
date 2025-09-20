import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)

class EmailSender:
    def __init__(self, config: 'Config'):
        self.config = config
    def render_template(self, template_path: str, data: dict[str, Any]) -> str:
        with open(template_path, 'r') as f:
            template = Template(f.read())
        return template.render(data)
        return template.render(data)

    def send_email(self, subject: str, to_email: str, name: str):
        html_content = self.render_template('email_template.html', {'name': name})

        msg = MIMEMultipart()
        msg['From'] = self.config.FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_content, 'html'))
        
        try:
            server = smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT)
            server.starttls()
            server.login(self.config.FROM_EMAIL, self.config.PASSWORD)
            text = msg.as_string()
            server.sendmail(self.config.FROM_EMAIL, to_email, text)
            server.quit()
            logging.info(f'Email sent to {to_email}')
        except Exception as e:
            logging.error(f'Error sending email: {e}')

if __name__ == '__main__':
    from config import Config
    config = Config()
    email_sender = EmailSender(config)
    email_sender.send_email('Test HTML Email', 'recipient-email@example.com', 'John')