import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import cv2
import requests
import webbrowser

# Initialize the speech recognition and text-to-speech engines
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening.....(speak now)")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            return command
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def get_weather(city):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    weather_data = response.json()
    weather = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    return f"The weather in {city} is {weather} with a temperature of {temperature} degrees Celsius."

def get_news():
    api_key = "YOUR_NEWS_API_KEY"
    response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}")
    news_data = response.json()
    headlines = [article["title"] for article in news_data["articles"]]
    return headlines

def run_assistant():
    talk("Hello, I'm your personal assistant. How can I help you?")
    while True:
        command = take_command()
        print(command)

        if "play" in command:
            song = command.replace("play", "")
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)
        elif "time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            talk(f"The current time is {time}")
        elif "date" in command:
            date = datetime.date.today()
            talk(f"Today's date is {date}")
        elif "joke" in command:
            talk(pyjokes.get_joke())
        elif "how are you" in command:
            talk("I'm good, thanks for asking!")
        elif "capture photo" in command or "take a photo" in command:
            talk("Smile and say cheese!")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cv2.imwrite("photo.jpg", frame)
            cap.release()
            cv2.destroyAllWindows()
            talk("Photo captured!")
        elif "record video" in command or "capture video" in command:
            talk("Press 's' to stop recording")
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
            while True:
                ret, frame = cap.read()
                out.write(frame)
                cv2.imshow("frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            talk("Video recorded!")
        elif "weather" in command:
            city = command.replace("weather in ", "")
            talk(get_weather(city))
        elif "news" in command:
            headlines = get_news()
            talk("Here are the latest news headlines:")
            for headline in headlines:
                talk(headline)
        elif "open google" in command:
            talk("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "exit" in command or "quit" in command:
            talk("Goodbye!")
            break
        else:
            talk("I didn't understand that. Can you please repeat?")

if __name__ == "__main__":
    run_assistant()
    