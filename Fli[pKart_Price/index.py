import requests
import base64
import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Flipkart API credentials
client_id = "__CLIENT_ID__"
client_secret = "__CLIENT_SECRET__"
sku_id = "__SKU_ID__"
threshold_price = "__THRESHOLD_PRICE__"

# Email notification settings
sender_email = "__SENDER_EMAIL__"
receiver_email = "__RECEIVER_EMAIL__"
password = "__PASSWORD__"
smtp_server = "__SMTP_SERVER__"
smtp_port = "__SMTP_PORT__"

def get_access_token():
    """Generate access token using Client Credentials Flow"""
    url = "https://api.flipkart.net/oauth-service/oauth/token"
    querystring = {"grant_type": "client_credentials", "scope": "Seller_Api"}
    headers = {
        'Authorization': "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    response_json = requests.request("GET", url, headers=headers, params=querystring).json()
    return response_json["access_token"]

def get_current_price(access_token):
    """Get current price of the product"""
    url = f"https://api.flipkart.net/sellers/skus/{sku_id}/listings"
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()["attributeValues"]["selling_price"]

def send_notification(price):
    """Send email notification when price drops below threshold"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Price Drop Alert!"
    body = f"Price dropped to {price}! Buy now!"
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

def check_price():
    """Check price and send notification if necessary"""
    access_token = get_access_token()
    current_price = get_current_price(access_token)
    if float(current_price) <= float(threshold_price):
        send_notification(current_price)
        print("Price dropped below threshold!")

# Schedule price check every hour
schedule.every(1).hour.do(check_price)

while True:
    schedule.run_pending()
    time.sleep(1)