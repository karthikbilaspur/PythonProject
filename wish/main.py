import os
import csv
import argparse
import smtplib
import datetime
import time
from typing import Dict, List
from email.mime.text import MIMEText

from dotenv import load_dotenv
load_dotenv()

CSV_FILE = "birthdays.csv"
SENT_LOG = "sent_log.txt"
HEADERS = ["id", "name", "email", "month", "day"]

# ---------- CSV MANAGEMENT ----------

def ensure_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
        print(f"[INFO] Created {CSV_FILE}")

def get_next_id():
    ensure_csv()
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        ids = [int(r['id']) for r in reader if r.get('id','').isdigit()]
        return max(ids) + 1 if ids else 1

def add_birthday(name: str, email: str, month: str, day: str) -> int:
    ensure_csv()
    
    # prevent duplicate email
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['email'].lower() == email.lower():
                print(f"[SKIP] {email} already exists with ID {row['id']}")
                return int(row['id'])

    new_id = get_next_id()
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow({
            "id": new_id,
            "name": name.strip(),
            "email": email.strip().lower(),
            "month": int(month),
            "day": int(day)
        })
    print(f"[ADDED] [{new_id}] {name} ({email}) - {month}/{day}")
    return new_id

def list_birthdays():
    ensure_csv()
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        if not rows:
            print("No birthdays yet. Use --add to add one.")
            return
        print(f"\n{'ID':<4} {'Name':<20} {'Email':<30} {'Birthday'}")
        print("-"*70)
        for r in rows:
            print(f"{r['id']:<4} {r['name']:<20} {r['email']:<30} {r['month']}/{r['day']}")

def delete_birthday(bid: int) -> None:
    ensure_csv()
    rows: List[Dict[str, str]] = []
    deleted = False
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['id'] == str(bid):
                deleted = True
                continue
            rows.append(r)
    
    if not deleted:
        print(f"[ERROR] ID {bid} not found")
        return

    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[DELETED] ID {bid}")

# ---------- EMAIL ----------

def send_email(to: str, name: str):
    from_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASS")
    
    if not from_email or not app_password:
        print("[ERROR] Set EMAIL_USER and EMAIL_PASS in .env file")
        return False

    subject = "Happy Birthday!"
    body = f"Dear {name},\n\nHappy Birthday! Wishing you a wonderful day filled with love, laughter, and all your favorite things.\n\nBest regards,\nKarthik"

    msg = MIMEText(body, 'plain')
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, app_password)
            server.sendmail(from_email, to, msg.as_string())
        print(f"[SENT] Birthday wish to {name} <{to}>")
        return True
    except Exception as e:
        print(f"[FAILED] {name} ({to}): {e}")
        return False

# ---------- CHECK LOGIC ----------

def has_sent_today(email: str, today_str: str):
    if not os.path.exists(SENT_LOG):
        return False
    with open(SENT_LOG, 'r') as f:
        return f"{today_str}:{email.lower()}" in f.read()

def mark_sent(email: str, today_str: str):
    with open(SENT_LOG, 'a') as f:
        f.write(f"{today_str}:{email.lower()}\n")

def check_birthdays():
    ensure_csv()
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            birthdays = list(csv.DictReader(f))
    except Exception as e:
        print(f"[ERROR] Reading CSV: {e}")
        return

    if not birthdays:
        print("[INFO] No birthdays in file.")
        return

    today = datetime.date.today()
    today_str = today.isoformat()
    is_leap = today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0)

    print(f"[CHECK] Today is {today} - checking {len(birthdays)} contacts...")
    sent_count = 0

    for row in birthdays:
        try:
            m = int(row['month'])
            d = int(row['day'])
            
            is_birthday = (m == today.month and d == today.day)
            
            # Celebrate Feb 29 on Feb 28 in non-leap years
            if not is_leap and m == 2 and d == 29 and today.month == 2 and today.day == 28:
                is_birthday = True

            if is_birthday:
                if has_sent_today(row['email'], today_str):
                    print(f"[SKIP] Already sent to {row['name']} today")
                    continue
                if send_email(row['email'], row['name']):
                    mark_sent(row['email'], today_str)
                    sent_count += 1
        except Exception as e:
            print(f"[ERROR] Row {row}: {e}")
    
    if sent_count == 0:
        print("[INFO] No birthdays today.")
    else:
        print(f"[DONE] Sent {sent_count} wishes.")

def add_interactive():
    print("\n--- Add New Birthday ---")
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    month = input("Month (1-12): ").strip()
    day = input("Day (1-31): ").strip()
    if not all([name, email, month, day]):
        print("[ERROR] All fields required!")
        return
    add_birthday(name, email, month, day)

# ---------- MAIN ----------

def main():
    parser = argparse.ArgumentParser(description="Auto Birthday Wisher")
    parser.add_argument("--add", action="store_true", help="Add birthday interactively")
    parser.add_argument("--list", action="store_true", help="List all birthdays")
    parser.add_argument("--delete", type=int, help="Delete by ID (e.g. --delete 2)")
    parser.add_argument("--check", action="store_true", help="Check and send wishes now")
    parser.add_argument("--loop", action="store_true", help="Run daily loop (checks every 24h at 9am)")

    args = parser.parse_args()
    ensure_csv()

    if args.add:
        add_interactive()
    elif args.list:
        list_birthdays()
    elif args.delete is not None:
        delete_birthday(args.delete)
    elif args.loop:
        while True:
            check_birthdays()
            # sleep until 9am next day
            now = datetime.datetime.now()
            tomorrow = now + datetime.timedelta(days=1)
            next_run = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            if now.hour < 9:
                next_run = now.replace(hour=9, minute=0, second=0, microsecond=0)
            secs = (next_run - now).total_seconds()
            print(f"Next check at {next_run} - sleeping {int(secs//3600)}h")
            time.sleep(secs)
    else:
        # default: --check
        check_birthdays()

if __name__ == "__main__":
    main()