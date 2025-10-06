import langdetect
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os

class LanguageDetector:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.translator = Translator()

    def recognize_speech(self, prompt):
        with self.microphone as source:
            print(prompt)
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return None

    def detect_language(self, text):
        try:
            language = langdetect.detect(text)
            return language
        except langdetect.lang_detect_exception.LangDetectException:
            print("Unable to detect language.")
            return None

    def translate_text(self, text, from_lang, to_lang):
        try:
            translation = self.translator.translate(text, src=from_lang, dest=to_lang)
            return translation.text
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            return None

    def text_to_speech(self, text, lang):
        try:
            speak = gTTS(text=text, lang=lang, slow=False)
            speak.save("translated_text.mp3")
            os.system("start translated_text.mp3")
        except Exception as e:
            print(f"An error occurred during text-to-speech conversion: {e}")

def get_language_code(prompt):
    while True:
        lang_code = input(prompt)
        if lang_code in LANGUAGES:
            return lang_code
        else:
            print("Invalid language code. Please try again.")

def main():
    detector = LanguageDetector()
    print("Language Translation System")
    print("-------------------------------")
    text = detector.recognize_speech("Speak a sentence to translate:")
    if text:
        print(f"Recognized text: {text}")
        language = detector.detect_language(text)
        if language:
            print(f"Detected language: {LANGUAGES[language]} ({language})")
            to_lang = get_language_code("Enter target language code (e.g., 'en' for English): ")
            translated_text = detector.translate_text(text, language, to_lang)
            if translated_text:
                print(f"Translated text: {translated_text}")
                detector.text_to_speech(translated_text, to_lang)
            else:
                print("Translation failed.")
        else:
            print("Language detection failed.")
    else:
        print("Speech recognition failed.")

if __name__ == "__main__":
    main()