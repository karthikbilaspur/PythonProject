# Import necessary libraries
from twilio.rest import Client
import schedule
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Twilio account details
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)
twilio_phone_number = 'your_twilio_phone_number'

# Function to send SMS
def send_sms(to: str, message: str):
    try:
        msg = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=to
        )
        logging.info(f'SMS sent to {to}: {msg.sid}')
    except Exception as e:
        logging.error(f'Error sending SMS: {e}')

# Function to send daily SMS
from typing import NoReturn

def send_daily_sms() -> None:
    to_phone_number = '+1234567890'  # Replace with recipient's phone number
    message_body = 'Good morning!'
    send_sms(to_phone_number, message_body)

# Function to send SMS with custom message and recipient
def send_custom_sms():
    to_phone_number = input('Enter recipient phone number: ')
    message_body = input('Enter message: ')
    send_sms(to_phone_number, message_body)
schedule.every().day.at("08:00").do(lambda: send_daily_sms())  # Send SMS at 8am daily
# Schedule daily SMS
schedule.every().day.at("08:00").do(send_daily_sms)  # Send SMS at 8am daily

# Main menu
def main_menu():
    while True:
        print('\nSMS Automation Menu:')
        print('1. Send daily SMS')
        print('2. Send custom SMS')
        print('3. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            send_daily_sms()
        elif choice == '2':
            send_custom_sms()
        elif choice == '3':
            break
        else:
            print('Invalid choice. Please try again.')

# Run scheduler and main menu
if __name__ == '__main__':
    import threading
    scheduler_thread = threading.Thread(target=lambda: schedule.run_pending() or time.sleep(1) or schedule.run_pending())
    scheduler_thread.daemon = True
    scheduler_thread.start()
    main_menu()