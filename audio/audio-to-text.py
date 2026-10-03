"""
audio-to-text.py - Convert spoken audio (WAV) to text using Google Speech Recognition.
Can run standalone with GUI or CLI.
"""
import argparse
import importlib
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from typing import Any

try:
    sr: Any = importlib.import_module("speech_recognition")
except ImportError:
    sr = None

class AudioToTextConverter:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Audio to Text Converter")
        self.root.geometry("600x350")
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text="Select Audio File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry = tk.Entry(self.root, width=50)
        self.entry.grid(row=0, column=1, padx=5, pady=10)

        tk.Button(self.root, text="Browse", command=self.select_audio_file).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Convert to Text", command=self.convert_audio_to_text).grid(row=1, column=1, pady=10)

        self.text_box = tk.Text(self.root, height=10, width=70)
        self.text_box.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=580, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def select_audio_file(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav"), ("All files", "*.*")])
        if file_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, file_path)

    def convert_audio_to_text(self, file_path: str | None = None) -> str | None:
        if file_path is None:
            file_path = self.entry.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select an audio file.")
            return None

        if sr is None:
            messagebox.showerror("Error", "speech_recognition library not installed. Run: pip install SpeechRecognition")
            return None

        try:
            self.progress_bar['value'] = 10
            self.root.update_idletasks()
            recognizer = sr.Recognizer()
            with sr.AudioFile(file_path) as source:
                self.progress_bar['value'] = 30
                audio_data = recognizer.record(source)
                self.progress_bar['value'] = 60
                self.root.update_idletasks()
                text = recognizer.recognize_google(audio_data)
                self.progress_bar['value'] = 100
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, text)
                return text
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio.")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"API Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.progress_bar['value'] = 0

def transcribe_cli(input_path: str) -> str:
    """CLI version without GUI"""
    if sr is None:
        raise ImportError("Install SpeechRecognition: pip install SpeechRecognition")
    r = sr.Recognizer()
    with sr.AudioFile(input_path) as source:
        audio = r.record(source)
        text = r.recognize_google(audio)
        print(f"Transcription: {text}")
        return text

def main():
    parser = argparse.ArgumentParser(description="Audio to Text Converter")
    parser.add_argument('-i', '--input', type=str, help='Input WAV file (CLI mode)')
    parser.add_argument('--gui', action='store_true', help='Launch GUI')
    args = parser.parse_args()

    if args.input:
        transcribe_cli(args.input)
    else:
        root = tk.Tk()
        _app = AudioToTextConverter(root)
        root.mainloop()

if __name__ == "__main__":
    main()
