import tkinter as tk
from tkinter import messagebox
import requests

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        # City input
        self.city_label = tk.Label(root, text="City:")
        self.city_label.pack()
        self.city_entry = tk.Entry(root)
        self.city_entry.pack()

        # API key input
        self.api_key_label = tk.Label(root, text="API Key:")
        self.api_key_label.pack()
        self.api_key_entry = tk.Entry(root, show="*")
        self.api_key_entry.pack()

        # Get weather button
        self.get_weather_button = tk.Button(root, text="Get Weather", command=self.display_weather)
        self.get_weather_button.pack()

        # Weather display
        self.weather_label = tk.Label(root, text="")
        self.weather_label.pack()

        # Additional info display
        self.additional_info_label = tk.Label(root, text="")
        self.additional_info_label.pack()

        # Save API key checkbox
        self.save_api_key = tk.BooleanVar()
        self.save_api_key_checkbox = tk.Checkbutton(root, text="Save API Key", variable=self.save_api_key)
        self.save_api_key_checkbox.pack()

    def get_weather(self, city, api_key):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        return response.json()

    def display_weather(self):
        city = self.city_entry.get()
        api_key = self.api_key_entry.get()
        weather_data = self.get_weather(city, api_key)

        if 'main' in weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            feels_like = weather_data['main']['feels_like']
            weather_description = weather_data['weather'][0]['description']

            self.weather_label.config(text=f"Weather in {city}: {temp}°C, Humidity: {humidity}%")
            self.additional_info_label.config(text=f"Feels like: {feels_like}°C, Description: {weather_description}")

            if self.save_api_key.get():
                # Save API key to a file or database
                with open("api_key.txt", "w") as f:
                    f.write(api_key)
        else:
            messagebox.showerror("Error", "Failed to retrieve weather data")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()