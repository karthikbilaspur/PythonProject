# Smart Photo Cleaner - Safe Edition

A 100% safe, offline, Python project that cleans your photo gallery using Face Detection.
No Facebook scraping, no TOS violation.

## Features
- Secure User Dashboard with Registration/Login
- Passwords hashed with Werkzeug (bcrypt)
- Email credentials stored in .env (never in DB)
- SQLite DB with SQLAlchemy ORM
- Photo Processor: Detects face, eyes open -> Marks as BEST
- History of all processed photos per user
- Unit tests with pytest

## Project Structure
```
smart_photo_cleaner/
├── app.py                 # Flask main app
├── models.py              # User + PhotoJob models
├── config.py              # Env config
├── utils/
│   └── photo_processor.py # Core face detection logic
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── tests/
│   ├── test_auth.py
│   └── test_photo_processor.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. Clone / Unzip
2. Create venv:
   python -m venv venv
   source venv/bin/activate (Linux) / venv\Scripts\activate (Windows)

3. Install:
   pip install -r requirements.txt

4. Env:
   cp .env.example .env
   Edit .env with your secret key and mail app password

5. Run:
   python app.py
   Open http://127.0.0.1:5000

## Run Tests
pytest -v

## Security Notes
- Passwords are NEVER stored in plain text
- Mail password is in .env only, not in DB
- face_recognition library recommended for production (more accurate than haarcascade)
- For Gmail, use App Password, not main password

## Future Improvements
- Replace haarcascade with mediapipe / DeepFace for emotion
- Add Streamlit frontend
- Add zip download of best_shots
- Add email report: "You have 200 best photos"
