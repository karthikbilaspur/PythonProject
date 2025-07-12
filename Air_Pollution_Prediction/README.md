Weather Data Retrieval and Analysis
Overview
This project uses the OpenWeatherMap API to retrieve current weather data for specified cities and provides features to display the data, save it to a CSV file, and plot a temperature comparison graph.
Features
Retrieves current weather data for specified cities using the OpenWeatherMap API
Displays weather data in a user-friendly format
Saves weather data to a CSV file
Plots a temperature comparison graph for multiple cities
Requirements
Python 3.x
requests library
csv library
matplotlib library
OpenWeatherMap API key
Installation
Clone the repository: git clone https://github.com/your-username/weather-data-retrieval.git
Install the required libraries: pip install requests matplotlib
Get an OpenWeatherMap API key: https://openweathermap.org/api
Usage
Run the script: python weather_data_retrieval.py
Enter your OpenWeatherMap API key when prompted
Choose an action:
Get current weather data: Enter 1 and specify the city name
Save weather data to CSV: Enter 2, specify the city name, and enter the filename (optional)
Plot temperature comparison graph: Enter 3 and specify the city names separated by commas
Quit: Enter 4
CSV File Format
The CSV file will have the following columns:
City: The name of the city
Temperature: The current temperature in the city
Feels Like: The temperature that it feels like in the city
Humidity: The humidity level in the city
Weather Condition: A brief description of the current weather condition
Notes
Make sure to replace your-username with your actual GitHub username in the clone command.
The API key is stored in plain text for simplicity, but it's recommended to use a secure method to store API keys in production environments.
The temperature comparison graph will display the temperatures for each city in a bar chart.
Contributing
Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.