import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

class AudioToTextConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio to Text Converter")
        self.create_widgets()

    def create_widgets(self):
        # Create labels and entry fields
        label = tk.Label(self.root, text="Select Audio File:")
        label.grid(row=0, column=0, padx=5, pady=5)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        # Create browse button
        button = tk.Button(self.root, text="Browse", command=self.select_audio_file)
        button.grid(row=0, column=2, padx=5, pady=5)

        # Create convert button
        convert_button = tk.Button(self.root, text="Convert to Text", command=self.convert_audio_to_text)
        convert_button.grid(row=1, column=1, padx=5, pady=5)

        # Create text box
        self.text_box = tk.Text(self.root, height=10, width=60)
        self.text_box.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Create progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, file_path)

    def convert_audio_to_text(self):
        file_path = self.entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select an audio file.")
            return

        try:
            self.progress_bar['value'] = 0
            r = sr.Recognizer()
            with sr.AudioFile(file_path) as source:
                audio = r.record(source)
            self.progress_bar['value'] = 50
            text = r.recognize_google(audio)
            self.progress_bar['value'] = 100
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, text)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Speech recognition could not understand the audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results from Google Speech Recognition service.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioToTextConverter(root)
    root.mainloop()