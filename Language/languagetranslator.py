import speech_recognition as spr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os

# Creating Recogniser() class object
recog1 = spr.Recognizer()

# Creating microphone instance
mc = spr.Microphone()

# Function to capture voice and recognize text
def recognize_speech(recog, source):
    try:
        recog.adjust_for_ambient_noise(source, duration=0.2)  # Adjust for background noise
        audio = recog.listen(source)  # Capture audio input
        recognized_text = recog.recognize_google(audio, language='en-US')  # Recognize using Google's recognizer
        return recognized_text.lower()
    except spr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        return None
    except spr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Function to translate text
def translate_text(text, from_lang, to_lang):
    translator = Translator()
    try:
        text_to_translate = translator.translate(text, src=from_lang, dest=to_lang)
        return text_to_translate.text
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

# Function to convert text to speech
def text_to_speech(text, lang):
    try:
        speak = gTTS(text=text, lang=lang, slow=False)
        speak.save("captured_voice.mp3")
        os.system("start captured_voice.mp3")
    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")

# Capture initial voice
with mc as source:
    print("Speak 'hello' to initiate the Translation!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    MyText = recognize_speech(recog1, source)

# Check if the input contains 'hello'
if MyText and 'hello' in MyText:
    # Source and target languages
    from_lang = input("Enter the source language code (e.g., 'en' for English): ")
    to_lang = input("Enter the target language code (e.g., 'hi' for Hindi): ")

    # Validate language codes
    if from_lang not in LANGUAGES or to_lang not in LANGUAGES:
        print("Invalid language code. Please check the language codes.")
    else:
        with mc as source:
            print("Speak a sentence to translate...")
            get_sentence = recognize_speech(recog1, source)

            # If sentence recognized properly
            if get_sentence:
                print(f"Phrase to be Translated: {get_sentence}")
                translated_text = translate_text(get_sentence, from_lang, to_lang)

                if translated_text:
                    print(f"Translated Text: {translated_text}")
                    text_to_speech(translated_text, to_lang)
                else:
                    print("Translation failed.")
            else:
                print("Unable to capture the sentence for translation.")