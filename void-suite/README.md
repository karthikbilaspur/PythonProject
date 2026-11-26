# Voice + Yoda Suite

Merged your 3 files into ONE runnable file.

 Files

- `index.py` - main file (run this)
- `requirements.txt` - optional libraries for mic/speaker modes
- `README.md` - this file

 How to Run

bash

Yoda mode works with ZERO install
python index.py

For Voice Assistant + GUI modes, install first:
pip install SpeechRecognition pyttsx3 PyAudio
Windows PyAudio if above fails:
pip install pipwin && pipwin install pyaudio

 Requirements

- Python 3.8+
- `tkinter` - usually included with Python (on Linux: `sudo apt install python3-tk`)
- Mic + internet needed for speech recognition (uses Google API)
- `SpeechRecognition`, `pyttsx3`, `PyAudio` - only for Modes 2 & 3
