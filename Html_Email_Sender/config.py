import os

class Config:
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'your-email@gmail.com')
    PASSWORD = os.environ.get('PASSWORD', 'your-password')