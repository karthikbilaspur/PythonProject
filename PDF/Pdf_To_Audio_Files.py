from PyPDF2 import PdfReader
from gtts import gTTS
import os

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ''
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def convert_text_to_audio(text, audio_file):
    try:
        audio = gTTS(text=text, lang='en', slow=False)
        audio.save(audio_file)
        return True
    except Exception as e:
        print(f"Error converting text to audio: {e}")
        return False

def pdf_to_audio(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    if text is None:
        return False

    audio_file = os.path.splitext(pdf_file)[0] + '.mp3'
    if convert_text_to_audio(text, audio_file):
        print(f"Audio file saved as {audio_file}")
        return True
    else:
        return False

def main():
    while True:
        pdf_file = input("Enter the path to the PDF file (or 'q' to quit): ")
        if pdf_file.lower() == 'q':
            break
        if not os.path.exists(pdf_file):
            print("File not found. Please try again.")
            continue
        if not pdf_file.endswith('.pdf'):
            print("Invalid file format. Please select a PDF file.")
            continue
        if pdf_to_audio(pdf_file):
            print("PDF to audio conversion successful!")
        else:
            print("PDF to audio conversion failed.")

if __name__ == "__main__":
    main()