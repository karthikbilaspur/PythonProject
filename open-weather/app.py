from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Default: Bangalore - change this to test other cities
CITIES = {
    "Bangalore": (12.9716, 77.5946),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Chennai": (13.0827, 80.2707),
    "London": (51.5074, -0.1278),
    "New York": (40.7128, -74.0060),
}

def get_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params: dict[str, str | int | float] = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
        "hourly": "temperature_2m,precipitation_probability",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 7,
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def get_air_quality(lat: float, lon: float):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params: dict[str, str | int | float] = {
        "latitude": lat,
        "longitude": lon,
        "current": "pm2_5,pm10,us_aqi,ozone",
        "hourly": "pm2_5,us_aqi",
        "timezone": "auto",
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def aqi_advice(aqi: int | float | None) -> tuple[str, str]:
    if aqi is None:
        return "No AQI data", "gray"
    if aqi <= 50:
        return "Great day to go outside! Air is clean.", "green"
    if aqi <= 100:
        return "Okay for most people. Sensitive folks, keep it light.", "yellow"
    if aqi <= 150:
        return "Unhealthy for sensitive groups. Mask if you go out long.", "orange"
    if aqi <= 200:
        return "Unhealthy. Better to workout indoors today.", "red"
    return "Very unhealthy. Stay indoors if you can.", "darkred"

WEATHER_CODES = {
    0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅",
    3: "Overcast ☁️", 45: "Foggy 🌫️", 48: "Foggy 🌫️",
    51: "Light drizzle 🌧️", 61: "Light rain 🌧️", 63: "Rain 🌧️",
    65: "Heavy rain ⛈️", 71: "Light snow ❄️", 80: "Light showers 🌦️",
    95: "Thunderstorm ⛈️"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    city = request.form.get('city', 'Bangalore')
    lat, lon = CITIES.get(city, CITIES['Bangalore'])

    try:
        weather = get_weather(lat, lon)
        aq = get_air_quality(lat, lon)

        current = weather['current']
        daily = weather['daily']

        aqi = aq['current'].get('us_aqi')
        advice, color = aqi_advice(aqi)

        data = {
            'city': city,
            'temp': current['temperature_2m'],
            'feels_like': current['apparent_temperature'],
            'humidity': current['relative_humidity_2m'],
            'wind': current['wind_speed_10m'],
            'condition': WEATHER_CODES.get(current['weather_code'], "Unknown"),
            'pm25': aq['current'].get('pm2_5'),
            'pm10': aq['current'].get('pm10'),
            'aqi': aqi,
            'advice': advice,
            'advice_color': color,
            'forecast': list(zip(
                daily['time'],
                daily['temperature_2m_max'],
                daily['temperature_2m_min'],
                daily['precipitation_probability_max']
            ))
        }
        error = None
    except Exception as e:
        data = None
        error = f"Could not fetch data: {e}"

    return render_template('index.html', cities=CITIES.keys(), selected=city, data=data, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=8000)