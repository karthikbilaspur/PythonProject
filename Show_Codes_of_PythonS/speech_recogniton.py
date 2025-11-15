import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import filedialog
import threading
import time
import os

class SpeechToText:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Speech to Text")
        self.label = tk.Label(text="Speech to Text Converter", font=("Helvetica", 16))
        self.label.pack()
        self.text_box = tk.Text(self.root, height=20, width=60)
        self.text_box.pack()
        self.button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.button.pack()
        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()
        self.save_button = tk.Button(self.root, text="Save to File", command=self.save_to_file)
        self.save_button.pack()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.audio_data = None

    def start_recording(self):
        self.listening = True
        self.button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.label.config(text="Recording...")
        threading.Thread(target=self.record_audio).start()

    def stop_recording(self):
        self.listening = False
        self.button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.label.config(text="Processing...")
        self.process_audio()

    def record_audio(self):
        with self.microphone as source:
            while self.listening:
                audio = self.recognizer.listen(source)
                if self.audio_data is None:
                    self.audio_data = audio
                else:
                    self.audio_data = self.combine_audio(self.audio_data, audio)

    def combine_audio(self, audio1, audio2):
        # Combine two audio data objects
        # This is a simple implementation and may not work perfectly
        # You may need to use a more advanced audio processing library
        # like pydub or soundfile
        import wave
        import io
        audio1_data = io.BytesIO(audio1.get_wav_data())
        audio2_data = io.BytesIO(audio2.get_wav_data())
        with wave.open(audio1_data, 'rb') as wav1, wave.open(audio2_data, 'rb') as wav2:
            params = wav1.getparams()
            data1 = wav1.readframes(wav1.getnframes())
            data2 = wav2.readframes(wav2.getnframes())
        combined_data = data1 + data2
        return sr.AudioData(combined_data, params[0], params[1], params[2], params[3])

    def process_audio(self):
        try:
            text = self.recognizer.recognize_google(self.audio_data)
            self.text_box.insert(tk.END, text + "\n")
            self.label.config(text="Speech to Text Converter")
        except sr.UnknownValueError:
            self.label.config(text="Could not understand audio")
        except sr.RequestError as e:
            self.label.config(text="Could not request results; {0}".format(e))

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_box.get("1.0", tk.END))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SpeechToText()
    app.run()