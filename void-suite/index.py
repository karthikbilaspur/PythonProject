"""
Voice + Yoda Suite - Merged from 3 files
  1. Yoda Speak Translator (no extra install needed)
  2. Voice Assistant (mic + speaker, needs: SpeechRecognition + pyttsx3 + PyAudio)
  3. Speech-to-Text GUI (Tkinter window, needs: SpeechRecognition)

Run: python index.py
"""

import random
import string
from typing import Any, cast

# ---------- 1. YODA SPEAK (from File 1, kept + improved) ----------
def speak_like_yoda(sentence: str) -> str:
    """Translate input sentence into Yoda-speak. Returns the new sentence."""
    sentence = sentence.lower()
    translator = str.maketrans('', '', string.punctuation.replace("'", ''))
    sentence = sentence.translate(translator)
    words = sentence.split()
    if not words:
        return "Speak, you must."
    random.shuffle(words)
    new_sent = ''
    for i, word in enumerate(words):
        if i == 0:
            new_sent += word.capitalize()
        elif i == len(words) - 1:
            new_sent += ' ' + word + '.'
        else:
            new_sent += ' ' + word
    yoda_phrases = [
        'A long time, I have waited.',
        'Much to learn, you still have.',
        'Patience, young one.',
        'Do or do not, there is no try.',
        'Strong with the Force, you are.',
        'Fear is the path to the dark side.',
    ]
    if random.random() < 0.5:
        new_sent += ' ' + random.choice(yoda_phrases)
    return new_sent

def yoda_mode():
    print("\n--- YODA MODE --- (type 'q' to go back)")
    while True:
        sentence = input("Enter your English sentence: ").strip()
        if sentence.lower() == 'q':
            break
        if not sentence:
            print("Empty, it is. Try again, you must.")
            continue
        result = speak_like_yoda(sentence)
        print(f"\nYour Yodenglish sentence:\n{result}\n")
        # NEW: Say it out loud if pyttsx3 is available
        try:
            import pyttsx3  # type: ignore[import-untyped]
            pyttsx3_module: Any = pyttsx3
            engine = cast(Any, pyttsx3_module.init())
            engine.say(result)
            engine.runAndWait()
        except Exception:
            pass  # No speaker lib = just print, no crash

# ---------- 2. VOICE ASSISTANT (from File 2) ----------
def voice_assistant_mode():
    try:
        import speech_recognition as sr  # type: ignore[import-untyped]
        import pyttsx3  # type: ignore[import-untyped]
        import datetime
    except ImportError as e:
        print(f"\nMissing library: {e}")
        print("Install with: pip install SpeechRecognition pyttsx3 PyAudio")
        print("On Windows PyAudio: pip install pipwin && pipwin install pyaudio")
        return
    engine = pyttsx3.init()
    def say(text: str):
        print(text)
        engine.say(text)
        engine.runAndWait()
    def recognize_speech() -> str | None:
        r: Any = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... (say hello / time / yoda / exit)")
            say("Listening...")
            # NEW: shorter listen + ambient adjustment so it doesn't hang
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            except Exception:
                print("No speech heard.")
                return None
            try:
                text: str = r.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                say("Sorry, could not understand audio")
            except sr.RequestError:
                say("Could not request results, check your internet connection")
        return None
    def process_command(text: str) -> bool:
        low = text.lower()
        if "hello" in low or "hi" in low:
            say("Hello! How can I assist you?")
        elif "time" in low:
            t = datetime.datetime.now().strftime("%H:%M")
            say(f"Current time is {t}")
        elif "date" in low:
            d = datetime.datetime.now().strftime("%d %B %Y")
            say(f"Today is {d}")
        elif "yoda" in low:
            # NEW: Cross-over - voice assistant + Yoda combined!
            say("Yoda mode, you want? Speak a sentence.")
            # Listen once more for the sentence
            s = recognize_speech()
            if s:
                result = speak_like_yoda(s)
                say(result)
        elif "exit" in low or "quit" in low or "bye" in low:
            say("Goodbye!")
            return False
        else:
            say("I heard you. Try hello, time, date, yoda, or exit.")
        return True
    print("\n--- VOICE ASSISTANT MODE --- Say 'exit' to go back")
    say("Voice assistant started.")
    while True:
        text = recognize_speech()
        if text:
            if not process_command(text):
                break

# ---------- 3. SPEECH-TO-TEXT GUI (from File 3, fixed) ----------
class SpeechToText:
    def __init__(self):
        try:
            import speech_recognition as sr  # type: ignore[import-untyped]
            import tkinter as tk
            from tkinter import filedialog
        except ImportError as e:
            print(f"Missing library: {e}")
            print("Install with: pip install SpeechRecognition PyAudio")
            self.root = None
            return
        import threading
        self.sr = sr
        self.tk = tk
        self.threading = threading
        self.filedialog = filedialog
        self.root = tk.Tk()
        self.root.title("Speech to Text + Yoda")
        self.root.geometry("620x520")
        tk.Label(self.root, text="Speech to Text Converter", font=("Helvetica", 16)).pack(pady=8)
        self.text_box = tk.Text(self.root, height=15, width=70)
        self.text_box.pack(padx=10)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.button = tk.Button(btn_frame, text="Start Recording", command=self.start_recording)
        self.button.grid(row=0, column=0, padx=5)
        self.stop_button = tk.Button(btn_frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Save to File", command=self.save_to_file).grid(row=0, column=2, padx=5)
        # NEW: Yoda button - converts last text to Yoda-speak
        tk.Button(btn_frame, text="Convert to Yoda!", command=self.convert_to_yoda).grid(row=0, column=3, padx=5)
        self.label = tk.Label(self.root, text="Press Start Recording", font=("Helvetica", 11))
        self.label.pack()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.audio_data = None

    def start_recording(self):
        self.listening = True
        self.audio_data = None
        self.button.config(state=self.tk.DISABLED)
        self.stop_button.config(state=self.tk.NORMAL)
        self.label.config(text="Recording... speak now")
        self.threading.Thread(target=self.record_audio, daemon=True).start()

    def stop_recording(self):
        self.listening = False
        self.button.config(state=self.tk.NORMAL)
        self.stop_button.config(state=self.tk.DISABLED)
        self.label.config(text="Processing...")
        self.process_audio()

    def record_audio(self):
        # FIXED: original loop never broke cleanly - now uses timeout
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            while self.listening:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    if self.audio_data is None:
                        self.audio_data = audio
                    else:
                        self.audio_data = self.combine_audio(self.audio_data, audio)
                except Exception:
                    continue

    def combine_audio(self, audio1: Any, audio2: Any):
        import wave, io
        a1 = io.BytesIO(audio1.get_wav_data())
        a2 = io.BytesIO(audio2.get_wav_data())
        with wave.open(a1, 'rb') as w1, wave.open(a2, 'rb') as w2:
            params = w1.getparams()
            data = w1.readframes(w1.getnframes()) + w2.readframes(w2.getnframes())
        return self.sr.AudioData(data, params[0], params[1])

    def process_audio(self):
        if self.audio_data is None:
            self.label.config(text="No audio recorded.")
            return
        try:
            text = cast(
                str,
                cast(Any, self.recognizer).recognize_google(self.audio_data),
            )
            self.text_box.insert(self.tk.END, text + "\n")
            self.label.config(text="Done! Press Start to record again.")
        except self.sr.UnknownValueError:
            self.label.config(text="Could not understand audio")
        except self.sr.RequestError as e:
            self.label.config(text=f"Could not request results: {e}")

    def convert_to_yoda(self):
        # NEW crossover: GUI text -> Yoda
        text = self.text_box.get("1.0", self.tk.END).strip()
        if not text:
            self.label.config(text="Nothing to convert. Record first!")
            return
        yoda = speak_like_yoda(text)
        self.text_box.insert(self.tk.END, f"\n[YODA] {yoda}\n")
        self.label.config(text="Converted to Yoda!")

    def save_to_file(self):
        file_path = self.filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.text_box.get("1.0", self.tk.END))

    def run(self):
        if self.root:
            self.root.mainloop()

def gui_mode():
    print("\nOpening Speech-to-Text GUI window... (close window to return to menu)")
    app = SpeechToText()
    app.run()

# ---------- MAIN MENU ----------
def main():
    print("="*52)
    print("  VOICE + YODA SUITE")
    print("="*52)
    while True:
        print("\nPick a mode:")
        print("  1. Yoda Speak Translator (works always, no mic needed)")
        print("  2. Voice Assistant (mic + speaker - say hello/time/yoda/exit)")
        print("  3. Speech-to-Text GUI (Tkinter window + Yoda button)")
        print("  q. Quit")
        choice = input("Enter 1 / 2 / 3 / q: ").strip().lower()
        if choice == 'q':
            print("May the Force be with you. Bye!")
            break
        elif choice == '1':
            yoda_mode()
        elif choice == '2':
            voice_assistant_mode()
        elif choice == '3':
            gui_mode()
        else:
            print("Invalid. Enter 1, 2, 3 or q.")

if __name__ == "__main__":
    main()
