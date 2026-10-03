# audio_convertor

All-in-one Python audio toolkit - Steganography + Speech-to-Text + Spectrogram Visualizer in one clean project.

Each module runs independently, and main.py runs them combined.

Project Structure
audio_convertor/
├── audio_steganography.py    Hide/extract secret text in WAV (LSB method)
├── audio_to_text.py          GUI + CLI speech recognition
├── audio_to_spectrogram.py   Audio -> Spectrogram image (librosa)
├── main.py                   Orchestrator - runs all 3 together
├── requirements.txt
└── README.md
Features Fixed from Original Code

1. Steganography Semantic Bug Fixed:

Old: Overwrote all 8 bits per byte -> destroyed audio
New: LSB only (byte & 254) | bit -> inaudible, professional
2. Added Safety Checks:

File existence, message length validation, proper delimiter END instead of 11111111
3. All 3 run solo:

bash
 Solo 1 - Stego

python audio_steganography.py -e -i input.wav -o secret.wav -m "hello"
python audio_steganography.py -d -i secret.wav

 Solo 2 - Speech to Text
python audio_to_text.py --gui
python audio_to_text.py -i speech.wav

 Solo 3 - Spectrogram
python audio_to_spectrogram.py -i song.wav -o spec.png -c inferno
4. Combined via main.py:

bash
 Interactive menu
python main.py

 Full pipeline (encode + 2 spectrograms + decode + transcription attempt)
python main.py --pipeline -i input.wav -m "my secret"

 Run only one from main
python main.py --stego-encode -i in.wav -o out.wav -m "hi"
python main.py --stego-decode -i out.wav
python main.py --to-text -i speech.wav
python main.py --to-spectrogram -i song.wav -o spec.png

Installation
bash

Requirements
Python 3.8+
wave (stdlib), librosa, matplotlib, SpeechRecognition, numpy
Naming Convention Used
All files use lowercase_with_underscore for Python modules (PEP8 correct) and repo is audio_convertor as requested. For GitHub best practice, rename folder to audio-converter (kebab-case).

License
MIT - Free to use for your portfolio.
