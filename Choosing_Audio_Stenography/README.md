Audio Steganography
A Python script that hides a secret message in an audio file using steganography.
Features
Audio Steganography: Hides a secret message in an audio file by modifying the least significant bits of the audio frames.
Message Encoding: Encodes the secret message in binary format and hides it in the audio file.
Message Decoding: Extracts the hidden message from the encoded audio file.
Requirements
Python 3.x: The script is designed to work with Python 3.x.
Wave Library: A built-in Python library for working with WAV audio files.
Usage
Encode Audio: Use the encode_audio function to hide a secret message in an audio file.
Decode Audio: Use the decode_audio function to extract the hidden message from an encoded audio file.