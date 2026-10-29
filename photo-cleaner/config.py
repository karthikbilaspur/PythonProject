import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///users.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    BEST_FOLDER = os.getenv("BEST_FOLDER", "best_shots")
    MAIL_EMAIL = os.getenv("MAIL_EMAIL")
    MAIL_APP_PASSWORD = os.getenv("MAIL_APP_PASSWORD")
