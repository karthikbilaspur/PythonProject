import requests
import csv
import matplotlib.pyplot as plt

def get_weather_data(city, api_key):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None

def display_weather_data(weather_data):
    if weather_data:
        print(f"Weather in {weather_data['name']}:")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Feels like: {weather_data['main']['feels_like']}°C")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Weather condition: {weather_data['weather'][0]['description']}")
    else:
        print("No weather data available.")

def save_weather_data_to_csv(weather_data, filename):
    if weather_data:
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['City', 'Temperature', 'Feels Like', 'Humidity', 'Weather Condition']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'City': weather_data['name'],
                'Temperature': weather_data['main']['temp'],
                'Feels Like': weather_data['main']['feels_like'],
                'Humidity': weather_data['main']['humidity'],
                'Weather Condition': weather_data['weather'][0]['description']
            })
        print(f"Weather data saved to {filename}.")
    else:
        print("No weather data available.")

def plot_temperature_graph(cities, api_key):
    temperatures = []
    for city in cities:
        weather_data = get_weather_data(city, api_key)
        if weather_data:
            temperatures.append(weather_data['main']['temp'])
        else:
            temperatures.append(0)

    plt.figure(figsize=(10, 6))
    plt.bar(cities, temperatures)
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Comparison')
    plt.show()

def main():
    api_key = input("Enter your OpenWeatherMap API key: ")
    while True:
        print("\n1. Get current weather data")
        print("2. Save weather data to CSV")
        print("3. Plot temperature comparison graph")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            city = input("Enter the city name: ")
            weather_data = get_weather_data(city, api_key)
            display_weather_data(weather_data)
        elif choice == '2':
            city = input("Enter the city name: ")
            filename = input("Enter the filename (default: weather_data.csv): ")
            if not filename:
                filename = 'weather_data.csv'
            weather_data = get_weather_data(city, api_key)
            save_weather_data_to_csv(weather_data, filename)
        elif choice == '3':
            cities = input("Enter the city names separated by comma: ").split(',')
            cities = [city.strip() for city in cities]
            plot_temperature_graph(cities, api_key)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()