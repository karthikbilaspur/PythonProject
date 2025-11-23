import os
import pyttsx3
import speech_recognition as sr
import tkinter.messagebox as tmessage
import wolframalpha
from os.path import exists

# Initialize speech recognition and text-to-speech engines
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Get Wolfram Alpha API token
wolfprimeaplahe_app = input('Enter the Wolfram Alpha API Token: ')

def speak(text: str) -> None:
    """Speak the given text"""
    engine.say(text)
    engine.runAndWait()

def welcome_message():
    """Display welcome message"""
    print('Welcome to Calculator :)')
    speak('Welcome to Calculator :)')
    print('If you want calculate something please tell calculate and then your expression')
    speak('If you want calculate something please tell calculate and then your expression')
    print('For example CALCULATE 7 PLUS 8 or CALCULATE sin30 plus cot20')
    speak('For example CALCULATE 7 PLUS 8 or CALCULATE sin30 plus cot20')

def recognize_speech() -> str:
    """Recognize speech and return the text"""
    with sr.Microphone() as source:
        print("Listening....")
        speak("Listening...")
        listener.pause_threshold = 2
        listener.energy_threshold = 3000
        audio = listener.listen(source)

    try:
        print("Recognizing...")
        speak("Recognizing...")
        query = listener.recognize_google(audio, language='en-In')
        print(query)
        return query
    except Exception as e:
        tmessage.showinfo('Error', f'{e}')
        print("Didn't understand you...\nCan you repeat?...")
        speak("Didn't understand you... Can you repeat?...")
        return "NONE"

def calculate(speech: str) -> None:
    """Calculate the given mathematical expression"""
    try:
        client = wolframalpha.Client(wolfprimeaplahe_app)
        indx = speech.lower().split().index('calculate')
        query = speech.split()[indx + 1:]
        res = client.query(''.join(query))
        answerr = next(res.results).text
        space = '\n'
        ourQuery = ''.join(query)
        Question = 'Your Query was :- '
        Answer = 'Your answer was :- '
        finalAnswer = Question + str(ourQuery) + space + Answer + str(answerr) + space

        if exists('./Voice Calculator/maths.txt'):
            with open('./Voice Calculator/maths.txt', 'a', encoding='utf-8') as mth:
                mth.write(finalAnswer)
                mth.close()
        else:
            history = open('./Voice Calculator/maths.txt', 'w', encoding='utf-8')
            history.write(finalAnswer)
            history.close()
        print("The answer is " + answerr)
        speak("the answer is %s" % answerr)
    except Exception as e:
        tmessage.showinfo('Error', f'{e}')
        print("Failed to calculate...\nPlease try again...")
        speak("Failed to calculate... Please try again...")

def clear_history() -> None:
    """Clear the calculation history"""
    try:
        if exists('./Voice Calculator/maths.txt'):
            with open('./Voice Calculator/maths.txt', 'r+') as file:
                file.truncate(0)
                file.close()
                print('History cleared...')
                speak('History cleared...')
        else:
            tmessage.showinfo('Error', 'No file exists with this name')
    except Exception as e:
        tmessage.showinfo('Error', f'{e}')
        print("Failed to clear history...\nPlease try again...")
        speak("Failed to clear history... Please try again...")

def show_history():
    """Show the calculation history"""
    try:
        if exists('./Voice Calculator/maths.txt'):
            os.system('./Voice Calculator/maths.txt')
        else:
            tmessage.showinfo('Error', 'No file exists with this name')
    except Exception as e:
        tmessage.showinfo('Error', f'{e}')
        print("Failed to show history...\nPlease try again...")
        speak("Failed to show history... Please try again...")

def main():
    welcome_message()
    while True:
        speech = recognize_speech().lower()
        if 'calculate' in speech:
            calculate(speech)
        elif 'clear' in speech:
            clear_history()
        elif 'history' in speech:
            show_history()
        elif 'quit' in speech or 'exit' in speech:
            break
        else:
            tmessage.showinfo('Opps', "Didn't understand")
            print("Didn't understand...\nPlease try again...")
            speak("Didn't understand... Please try again...")

if __name__ == "__main__":
    main()