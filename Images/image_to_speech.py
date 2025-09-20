import io
import os
from google.cloud import vision
from google.cloud import texttospeech
import tkinter as tk
from tkinter import filedialog

def image_to_text(image_path):
    try:
        client = vision.ImageAnnotatorClient()
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description if texts else None
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def text_to_speech(text, output_file):
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3
        )
        response = client.synthesize_speech(synthesis_input, voice, audio_config)
        with open(output_file, 'wb') as out:
            out.write(response.audio_content)
        print(f"Audio saved as {output_file}")
    except Exception as e:
        print(f"Error generating audio: {e}")

def main():
    root = tk.Tk()
    root.withTextvariable = tk.StringVar()
    root.withdraw()

    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", ".png .jpg .jpeg .bmp")])

    if image_path:
        text = image_to_text(image_path)
        if text:
            print("Extracted text:", text)
            output_file = filedialog.asksaveasfilename(title="Save Audio", defaultextension=".mp3", filetypes=[("MP3 Files", ".mp3")])
            if output_file:
                text_to_speech(text, output_file)
        else:
            print("No text found in the image.")

if __name__ == "__main__":
    main()
    