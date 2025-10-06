import io
import os
from google.cloud import vision
from google.cloud import texttospeech
import tkinter as tk
from tkinter import filedialog, ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image to Speech")
        self.geometry("500x300")

        self.image_path = tk.StringVar()
        self.text = tk.StringVar()
        self.voice = tk.StringVar()
        self.language = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Image selection
        tk.Label(self, text="Select Image:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self, textvariable=self.image_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Browse", command=self.browse_image).grid(row=0, column=2, padx=5, pady=5)

        # Language selection
        tk.Label(self, text="Select Language:").grid(row=1, column=0, padx=5, pady=5)
        languages = ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT"]
        language_menu = ttk.Combobox(self, textvariable=self.language)
        language_menu['values'] = languages
        language_menu.current(0)
        language_menu.grid(row=1, column=1, padx=5, pady=5)

        # Voice selection
        tk.Label(self, text="Select Voice:").grid(row=2, column=0, padx=5, pady=5)
        voices = ["NEUTRAL", "FEMALE", "MALE"]
        voice_menu = ttk.Combobox(self, textvariable=self.voice)
        voice_menu['values'] = voices
        voice_menu.current(0)
        voice_menu.grid(row=2, column=1, padx=5, pady=5)

        # Extract text button
        tk.Button(self, text="Extract Text", command=self.extract_text).grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Save audio button
        tk.Button(self, text="Save Audio", command=self.save_audio).grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # Object detection button
        tk.Button(self, text="Detect Objects", command=self.detect_objects).grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # Text display
        tk.Label(self, text="Extracted Text:").grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        tk.Text(self, height=5, width=50).grid(row=7, column=0, columnspan=3, padx=5, pady=5)

    def browse_image(self):
        path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", ".png .jpg .jpeg .bmp")])
        self.image_path.set(path)

    def extract_text(self):
        image_path = self.image_path.get()
        if image_path:
            try:
                client = vision.ImageAnnotatorClient()
                with io.open(image_path, 'rb') as image_file:
                    content = image_file.read()
                image = vision.Image(content=content)
                response = client.text_detection(image=image)
                texts = response.text_annotations
                self.text.set(texts[0].description if texts else "No text found")
                # Display extracted text
                text_box = self.winfo_children()[12]
                text_box.delete('1.0', tk.END)
                text_box.insert('1.0', self.text.get())
            except Exception as e:
                print(f"Error extracting text: {e}")

    def save_audio(self):
        text = self.text.get()
        if text:
            try:
                client = texttospeech.TextToSpeechClient()
                synthesis_input = texttospeech.SynthesisInput(text=text)
                voice = texttospeech.VoiceSelectionParams(
                    language_code=self.language.get(),
                    ssml_gender=getattr(texttospeech.enums.SsmlVoiceGender, self.voice.get())
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3
                )
                response = client.synthesize_speech(synthesis_input, voice, audio_config)
                output_file = filedialog.asksaveasfilename(title="Save Audio", defaultextension=".mp3", filetypes=[("MP3 Files", ".mp3")])
                if output_file:
                    with open(output_file, 'wb') as out:
                        out.write(response.audio_content)
                    print(f"Audio saved as {output_file}")
            except Exception as e:
                print(f"Error generating audio: {e}")

    def detect_objects(self):
        image_path = self.image_path.get()
        if image_path:
            try:
                client = vision.ImageAnnotatorClient()
                with io.open(image_path, 'rb') as image_file:
                    content = image_file.read()
                image = vision.Image(content=content)
                objects = client.object_localization(image=image).localized_object_annotations
                print("Detected objects:")
                for object_ in objects:
                    print(object_.name)
            except Exception as e:
                print(f"Error detecting objects: {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()