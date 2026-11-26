"""SMS Automation - Twilio + schedule.
Fixes: hardcoded placeholder credentials + Client at import -> crash (now env vars, lazy client); daily SMS scheduled TWICE -> now once; scheduler thread lambda ran once then exited -> now while True loop; hardcoded recipient -> SMS_TO env; E.164 validation."""
import logging, os, re, threading, time, schedule
from twilio.rest import Client  # pyright: ignore[reportMissingTypeStubs]
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
_client=None
def get_client():
    global _client
    if _client is None:
        sid,token=os.environ.get("TWILIO_ACCOUNT_SID"),os.environ.get("TWILIO_AUTH_TOKEN")
        if not sid or not token: raise RuntimeError("Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN env vars first.")
        _client=Client(sid,token)
    return _client
def send_sms(to: str, message: str):
    frm=os.environ.get("TWILIO_FROM")
    if not frm: logging.error("Set TWILIO_FROM env var."); return False
    if not re.fullmatch(r"\+\d{10,15}",to.strip()): logging.error(f"Invalid phone '{to}' - use E.164 like +919999999999."); return False
    if not message.strip(): logging.error("Message is empty."); return False
    try:
        m=get_client().messages.create(body=message,from_=frm,to=to.strip()); logging.info(f"SMS sent to {to}: {m.sid}"); return True
    except Exception as e: logging.error(f"Error sending SMS: {e}"); return False
def send_daily_sms() -> None: send_sms(os.environ.get("SMS_TO",""),"Good morning!")
def send_custom_sms():
    send_sms(input("Enter recipient (+countrycode...): ").strip(), input("Enter message: ").strip())
def _loop():
    while True: schedule.run_pending(); time.sleep(30)
def main_menu():
    t=os.environ.get("SMS_TIME","08:00")
    schedule.every().day.at(t).do(send_daily_sms)  # pyright: ignore[reportUnknownMemberType]  # scheduled exactly once
    logging.info(f"Daily SMS scheduled at {t} to {os.environ.get('SMS_TO','(SMS_TO not set)')}")
    threading.Thread(target=_loop,daemon=True).start()
    while True:
        print("\nSMS Automation Menu:\n1. Send daily SMS now\n2. Send custom SMS\n3. Exit")
        c=input("Enter your choice: ").strip()
        if c=="1": send_daily_sms()
        elif c=="2": send_custom_sms()
        elif c=="3": break
        else: print("Invalid choice.")
if __name__=="__main__": main_menu()
