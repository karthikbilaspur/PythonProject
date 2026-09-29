Virtual Assistant Chatbot README
Overview
This project implements a virtual assistant chatbot that can perform various tasks, such as:
Providing the current time and date
Retrieving the current weather for a given city
Fetching the latest news headlines for a given topic
Searching online for a given query
Responding to basic user queries, such as greetings and good_userbyes
Features
Time and Date: Provides the current time and date
Weather: Retrieves the current weather for a given city
News: Fetches the latest news headlines for a given topic
Search: Searches online for a given query
Conversational: Responds to basic user queries, such as greetings and good_userbyes
Requirements
Python 3.x
requests library (for making API calls)
webbrowser library (for searching online)
OpenWeatherMap API key (for retrieving weather data)
News API key (for fetching news headlines)
Installation
Clone the repository
Install the required libraries: pip install requests
Replace the placeholder API keys with your actual API keys
Usage
Run the project: python main.py
Interact with the chatbot by typing messages
Type 'quit' to exit the chatbot
API Endpoints
OpenWeatherMap API: http://api.openweathermap.org/data/2.5/weather
News API: https://newsapi.org/v2/everything