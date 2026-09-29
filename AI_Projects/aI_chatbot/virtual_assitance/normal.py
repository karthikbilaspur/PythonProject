import datetime
import random
import webbrowser
import requests

# Define a dictionary of intents and responses
intents = {
    "greeting": ["Hello! How can I assist you today?", "Hi there! What's on your mind?", "Hey, how's it going?"],
    "goodbye": ["See you later! Have a great day!", "Bye for now! Feel free to come back anytime.", "Goodbye! It was nice chatting with you."],
    "time": ["The current time is", "It's currently"],
    "date": ["Today's date is", "The current date is"],
    "weather": ["The current weather in {} is {}", "The weather in {} is currently {}"],
    "news": ["Here are the latest news headlines: {}", "I've found some news articles about {}"],
    "search": ["What would you like me to search for?", "What topic would you like to explore?"]
}

# Define a function to get the current time
def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

# Define a function to get the current date
def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Define a function to get the current weather
def get_weather(city):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    data = response.json()
    weather = data["weather"][0]["description"]
    return weather

# Define a function to get the latest news
def get_news(topic):
    api_key = "YOUR_NEWS_API_KEY"
    response = requests.get(f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}")
    data = response.json()
    articles = data["articles"]
    headlines = [article["title"] for article in articles]
    return headlines

# Define a function to search online
def search_online(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

# Define a function to respond to user input
def respond_to_input(input_text):
    input_text = input_text.lower()
    if "hello" in input_text or "hi" in input_text:
        return random.choice(intents["greeting"])
    elif "goodbye" in input_text or "bye" in input_text:
        return random.choice(intents["goodbye"])
    elif "time" in input_text:
        return f"{random.choice(intents['time'])} {get_time()}"
    elif "date" in input_text:
        return f"{random.choice(intents['date'])} {get_date()}"
    elif "weather" in input_text:
        city = input_text.replace("weather", "").strip()
        weather = get_weather(city)
        return f"{random.choice(intents['weather']).format(city, weather)}"
    elif "news" in input_text:
        topic = input_text.replace("news", "").strip()
        headlines = get_news(topic)
        return f"{random.choice(intents['news']).format(', '.join(headlines))}"
    elif "search" in input_text:
        query = input_text.replace("search", "").strip()
        search_online(query)
        return f"Searching for {query}..."
    else:
        return "I didn't understand that. Can you please rephrase?"

# Define a main function to run the chatbot
def main():
    print("Welcome to the virtual assistant chatbot! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = respond_to_input(user_input)
        print("Bot:", response)

# Run the main function
if __name__ == "__main__":
    main()