import wave
import argparse

DELIMITER = "#####END#####"

def text_to_binary(text: str) -> str:
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary: str) -> str:
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars if len(b) == 8)

def encode_audio(input_path: str, secret_message: str, output_path: str):
    audio = wave.open(input_path, 'rb')
    params = audio.getparams()
    frames = bytearray(audio.readframes(audio.getnframes()))
    audio.close()

    full_message = secret_message + DELIMITER
    binary_message = text_to_binary(full_message)

    if len(binary_message) > len(frames):
        raise ValueError(f"Message too long. Need {len(binary_message)} bytes, audio has {len(frames)} bytes capacity.")

    # LSB only - fix for semantic error (previous code overwrote all 8 bits)
    for i in range(len(binary_message)):
        frames[i] = (frames[i] & 254) | int(binary_message[i])

    encoded = wave.open(output_path, 'wb')
    encoded.setparams(params)
    encoded.writeframes(bytes(frames))
    encoded.close()
    print(f"[+] Encoded file saved: {output_path}")

def decode_audio(input_path: str) -> str:
    audio = wave.open(input_path, 'rb')
    frames = bytearray(audio.readframes(audio.getnframes()))
    audio.close()

    binary = ''.join(str(b & 1) for b in frames)
    
    # Convert to text in chunks and look for delimiter
    message = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        message += char
        if message.endswith(DELIMITER):
            return message[:-len(DELIMITER)]
    
    raise ValueError("No hidden message found or delimiter missing.")

def main():
    parser = argparse.ArgumentParser(description="Audio Steganography - LSB method")
    parser.add_argument('-e', '--encode', action='store_true', help='Encode mode')
    parser.add_argument('-d', '--decode', action='store_true', help='Decode mode')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input WAV file')
    parser.add_argument('-o', '--output', type=str, help='Output WAV file (for encode)')
    parser.add_argument('-m', '--message', type=str, help='Secret message to hide')
    args = parser.parse_args()

    if args.encode:
        if not args.output or not args.message:
            parser.error("Output file (-o) and message (-m) are required for encoding.")
        encode_audio(args.input, args.message, args.output)
    elif args.decode:
        msg = decode_audio(args.input)
        print(f"Decoded message: {msg}")
    else:
        parser.error("Choose either -e/--encode or -d/--decode")

if __name__ == "__main__":
    main()
