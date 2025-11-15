import speech_recognition as sr
import pyttsx3
import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()

def recognize_speech():
    # Create a recognizer object
    r = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")
        engine.say("Listening...")
        engine.runAndWait()
        audio = r.listen(source)

        try:
            # Recognize the speech
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            engine.say(f"You said: {text}")
            engine.runAndWait()
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio")
            engine.say("Sorry, could not understand audio")
            engine.runAndWait()
        except sr.RequestError:
            print("Could not request results; check your internet connection")
            engine.say("Could not request results; check your internet connection")
            engine.runAndWait()

def process_command(text: str) -> bool:
    if "hello" in text.lower():
        print("Hello! How can I assist you?")
        engine.say("Hello! How can I assist you?")
        engine.runAndWait()
    elif "time" in text.lower():
        current_time = datetime.datetime.now().strftime("%H:%M")
        print(f"Current time: {current_time}")
        engine.say(f"Current time is {current_time}")
        engine.runAndWait()
    elif "exit" in text.lower():
        print("Goodbye!")
        engine.say("Goodbye!")
        engine.runAndWait()
        return False
    return True

def main():
    while True:
        text = recognize_speech()
        if text:
            if not process_command(text):
                break

if __name__ == "__main__":
    main()