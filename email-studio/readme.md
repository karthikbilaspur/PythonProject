# 📧 MailForge Pro - Supabase Edition

Your 5 separate scripts → One deployable AI Email SaaS.

This repo now has NO Tkinter files. Pure Streamlit + Cloud DB.

✨ Features
Compose: To/CC/Subject/Body + drag-drop attachments
AI Studio: Gemini Flash / OpenAI GPT-4o-mini support (free tier) - fallback to smart templates
Security: MX validation (dnspython) + spam score + progress bar
Scheduler DB: Persistent scheduling that survives app restarts

🗄️ Database: SQLite vs Supabase
Mode When Persistence
SQLite (mailforge.db) Local streamlit run Lost on Streamlit Cloud restart
Postgres / Supabase When DATABASE_URL env/secret exists Permanent, works 24/7 in cloud
Code auto-detects:

DATABASE_URL = os.getenv("DATABASE_URL")  # if exists → Postgres, else SQLite
Supabase Setup (2 mins, free)
Go to [supabase.com](https://supabase.com) → New Project
Project Settings → Database → Connection String → URI
Copy: `postgresql://postgres.xxx:password@aws-0-ap-south-1.pooler.supabase.com:6543/postgres`
Add to Streamlit Cloud Secrets:

streamlit/secrets.toml

DATABASE_URL = `"postgresql://postgres.xxx:password@host:6543/postgres"`
SENDER_EMAIL = "you@gmail.com"
SENDER_APP_PASSWORD = "abcd efgh ijkl mnop"
GEMINI_API_KEY = "AIza..."
Tables are auto-created on first run:

scheduled_emails (id, to_emails, subject, body, schedule_time, repeat_type, status, created_at, last_sent)
sent_log (id, to_emails, subject, sent_at, status, error)
How Scheduling Works in Cloud
Local: Background thread checks every 60s and sends.
Cloud (Streamlit Cloud): App sleeps when no visitors. For true cron in cloud, add one of:
Option A (Free): Use GitHub Actions + curl [this trigger endpoint](https://yourapp.streamlit.app/api/trigger) every hour
Option B: Deploy background worker on Render/Railway that runs background_worker()
Option C: Switch to Supabase Cron extension (runs SQL that calls your email function)
For portfolio/demo, SQLite mode + manual "Start Background Sender" is enough.

🚀 Run
pip install -r requirements.txt
streamlit run mailforge.py
requirements.txt

streamlit
dnspython
google-generativeai
openai
psycopg2-binary
pandas
python-dotenv
📦 Deploy to Streamlit Cloud
Push mailforge_pro_streamlit.py + requirements.txt + README.md to GitHub
[share.streamlit.io](https://share.streamlit.io) → New App → Select repo
Paste Secrets (DATABASE_URL + Gmail + Gemini)
Deploy → You get [MailForge Pro](https://mailforge-pro.streamlit.app)
Your scheduled emails will now persist even after app restart because they're in Supabase Postgres, not local file.

🔐 Security vs Your Original Code
Raw sendmail(sender, to, body) → EmailMessage with proper headers
Plain password StringVar → st.secrets + App Passwords
SMTP RCPT probing (IP ban risk) → MX record check only
schedule blocking loop → DB + daemon thread
📸 Demo Flow for Recruiter
Compose → Validate → Spam Check
AI Studio → Generate cold outreach with Gemini
Schedule daily at 09:00 → Save to DB → Show Scheduled Queue (Postgres badge)
Sent Log shows history
Built as evolution from Tkinter to Web + Cloud DB.
