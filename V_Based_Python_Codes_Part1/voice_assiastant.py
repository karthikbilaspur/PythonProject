import os
import time
import speech_recognition as sr
import playsound
from gtts import gTTS
import random
import pyttsx3
import datetime
import webbrowser
from ecapture import ecapture as ec

def speak(text: str) -> None:
    """Speak the given text"""
    try:
        r1 = random.randint(1, 10000000)
        r2 = random.randint(1, 10000000)
        randfile = str(r2) + "randomtext" + str(r1) + ".mp3"
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(randfile)
        playsound.playsound(randfile)
        os.remove(randfile)
    except Exception as e:
        print(f"Error speaking: {e}")

def get_audio() -> str:
    """Recognize speech and return the text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say anything: ")
        audio = r.listen(source)
        try:
            said = r.recognize_google(audio)
            print(said)
            return said
        except sr.UnknownValueError:
            print("Sorry, could not recognize")
            speak("Sorry, could not recognize")
            return ""
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            speak("Error recognizing speech")
            return ""

def main():
    engine = pyttsx3.init()
    engine.say("Hello sir!, This is Robot, Created by Sai Harsha, How can I help you?")
    engine.runAndWait()

    while True:
        text = get_audio().lower()
        if text == "":
            continue

        if "ppt" in text or "intro" in text:
            engine.say("Yes sir, why not?")
            engine.runAndWait()
            os.system(r"d:\image.png")
        elif "google" in text:
            engine.say("Yes sir, why not?")
            engine.runAndWait()
            webbrowser.open("https://www.google.com")
        elif 'news' in text:
            engine.say('Here are some headlines from the Times of India, Happy reading')
            engine.runAndWait()
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            time.sleep(6)
        elif 'search' in text:
            text = text.replace("search", "")
            engine.say(f"Searching for {text}")
            engine.runAndWait()
            webbrowser.open_new_tab(text)
            time.sleep(5)
        elif 'time' in text:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            engine.say(f"The time is {strTime}")
            engine.runAndWait()
        elif 'open gmail' in text:
            engine.say("Opening Gmail")
            engine.runAndWait()
            webbrowser.open_new_tab("gmail.com")
            time.sleep(5)
        elif 'open youtube' in text:
            engine.say("Opening YouTube")
            engine.runAndWait()
            webbrowser.open_new_tab("https://www.youtube.com")
            time.sleep(5)
        elif "camera" in text or "take a photo" in text:
            engine.say("Taking a photo")
            engine.runAndWait()
            ec.capture(0, "robo camera", "img.jpg")
        elif 'quit' in text or 'exit' in text:
            break
        else:
            engine.say("Sorry, I didn't understand")
            engine.runAndWait()

if __name__ == "__main__":
    main()