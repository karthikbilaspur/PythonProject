import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes

# Initialize the speech recognition and text-to-speech engines
listener = sr.Recognizer()
engine = pyttsx3.init()

# Function to talk
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to wish the user
def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        talk("Good Morning!")
    elif hour >= 12 and hour < 18:
        talk("Good Afternoon!")
    else:
        talk("Good Evening!")
    talk("I am your voice assistant. How can I help you today?")

# Function to take voice command
def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            return command
    except:
        return ""

# Function to run the voice assistant
def run_assistant():
    wish_user()
    while True:
        command = take_command()
        if 'wikipedia' in command:
            talk("Searching Wikipedia...")
            command = command.replace("wikipedia", "")
            try:
                result = wikipedia.summary(command, sentences=2)
                talk("According to Wikipedia:")
                talk(result)
            except:
                talk("Sorry, I couldn't find anything.")
        elif 'open youtube' in command:
            talk("Opening YouTube...")
            webbrowser.open("https://www.youtube.com/")
        elif 'open google' in command:
            talk("Opening Google...")
            webbrowser.open("https://www.google.com/")
        elif 'time' in command:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            talk(f"The current time is {strTime}")
        elif 'joke' in command:
            joke = pyjokes.get_joke()
            talk(joke)
        elif 'exit' in command or 'bye' in command:
            talk("Goodbye! Have a nice day!")
            break
        else:
            talk("Sorry, I didn't understand that. Try again.")

# Main Function
def main():
    run_assistant()

if __name__ == "__main__":
    main()