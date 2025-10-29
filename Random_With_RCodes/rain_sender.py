import requests
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def get_location_coordinates(city: str) -> tuple[float, float]:
    """Get the latitude and longitude of a city."""
    api_endpoint = 'https://nominatim.openstreetmap.org/search.php'
    params = {
        'city': city,
        'format': 'json',
    }
    response = requests.get(api_endpoint, params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError(f"Unable to find location for {city}")
    return data[0]['lat'], data[0]['lon']

def get_weather_data(lat: float, lon: float, api_key: str) -> dict:
    """Get the weather data for a location."""
    api_endpoint = 'http://api.openweathermap.org/data/2.5/onecall'
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'exclude': 'current,minutely,daily',
    }
    response = requests.get(api_endpoint, params=params)
    response.raise_for_status()
    return response.json()

def send_email(subject: str, body: str, sender_email: str, sender_password: str, recipient_email: str):
    """Send an email."""
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['from'] = sender_email
    msg['to'] = recipient_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

def main():
    city = input('Enter your city: ')
    recipient_email = input('Send mail to (mail id): ')

    api_key = os.getenv('API_KEY')
    sender_email = os.getenv('MAIL')
    sender_password = os.getenv('PASSWORD')

    if not api_key or not sender_email or not sender_password:
        raise ValueError("API key or email credentials not found")

    try:
        lat, lon = get_location_coordinates(city)
        weather_data = get_weather_data(lat, lon, api_key)

        bring_umbrella = False
        for i in range(0, 12):
            hourly_condition = weather_data['hourly'][i]['weather'][0]['id']
            if hourly_condition < 700:
                bring_umbrella = True
                break

        if bring_umbrella:
            subject = "Rain Rain"
            body = "It's going to rain today. Bring Umbrella"
        else:
            subject = "Sunny Day"
            body = "May be a sunny day. Carry sunglasses."

        send_email(subject, body, sender_email, sender_password, recipient_email)
        print('Mail Sent')

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")

if __name__ == "__main__":
    main()