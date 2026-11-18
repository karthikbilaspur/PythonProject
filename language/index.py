import langdetect  # type: ignore
from deep_translator import GoogleTranslator  # type: ignore
import speech_recognition as sr  # type: ignore
from gtts import gTTS  # type: ignore
import os
import platform
import subprocess
from typing import Any, cast

# Supported languages - ne intha list la irunthu choose pannalam
LANGUAGES = {
    'en': 'English',
    'ta': 'Tamil',
    'hi': 'Hindi',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'kn': 'Kannada',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ja': 'Japanese'
}

class VoiceTranslator:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self, prompt: str = "Pesunga...") -> str | None:
        with sr.Microphone() as source:
            print(f"\n{prompt}")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                recognizer = cast(Any, self.recognizer)
                text = cast(str, recognizer.recognize_google(audio))
                print(f"Ne sonnathu: {text}")
                return text
            except sr.WaitTimeoutError:
                print("Yaarum pesala, thirumba try pannu")
            except sr.UnknownValueError:
                print("Puriyala da, thirumba sollu")
            except sr.RequestError:
                print("Internet problem da")
        return None

    def detect(self, text: str) -> str:
        try:
            detector = cast(Any, langdetect)
            lang = cast(str, detector.detect(text))
            return lang
        except Exception:
            return 'en'

    def translate(self, text: str, src: str, dest: str) -> str | None:
        try:
            translator = cast(Any, GoogleTranslator(source=src, target=dest))
            return cast(str, translator.translate(text))
        except Exception as e:
            print(f"Translate error: {e}")
            return None

    def speak(self, text: str, lang: str) -> None:
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            cast(Any, tts).save("translated.mp3")
            system = platform.system()
            if system == "Windows":
                subprocess.Popen(["explorer.exe", os.path.abspath("translated.mp3")])
            elif system == "Darwin":
                subprocess.call(["afplay", "translated.mp3"])
            else:
                subprocess.call(["xdg-open", "translated.mp3"])
        except Exception as e:
            print(f"Voice error: {e}")

def get_target_lang():
    print("\nLanguage List:")
    for code, name in LANGUAGES.items():
        print(f"{code} - {name}")
    while True:
        code = input("\nTarget language code kudunga (ex: ta, en, hi): ").strip().lower()
        if code in LANGUAGES:
            return code
        print("Thappu code da, list la irunthu kudunga")

def main():
    app = VoiceTranslator()
    print("=== VOICE TRANSLATOR - UPDATED ===")
    print("Veliya vara 'exit' nu sollunga")
    
    to_lang = get_target_lang()
    print(f"\nTarget: {LANGUAGES[to_lang]} - Ready da!")

    while True:
        text = app.listen("Pesunga...")
        if not text:
            continue
        if 'exit' in text.lower():
            print("Bye da! 👋")
            break

        src = app.detect(text)
        print(f"Detected Language: {LANGUAGES.get(src, src)} ({src})")
        
        translated = app.translate(text, src, to_lang)
        if translated:
            print(f"Translated: {translated}")
            app.speak(translated, to_lang)

if __name__ == "__main__":
    main()