import wave
import argparse

def encode_audio(file_path, secret_message, output_file):
    # Open the audio file
    audio = wave.open(file_path, 'rb')
    params = audio.getparams()
    frames = audio.readframes(audio.getnframes())

    # Convert the secret message to binary
    binary_message = ''.join(format(ord(c), '08b') for c in secret_message)
    binary_message += '11111111'  # Add a delimiter to mark the end of the message

    # Check if the audio file is long enough to hide the message
    if len(frames) * 8 < len(binary_message):
        raise Exception("Audio file is too short to hide the message.")

    # Hide the message in the audio file
    encoded_frames = bytearray(frames)
    message_index = 0
    for i in range(len(encoded_frames)):
        for j in range(8):
            if message_index < len(binary_message):
                encoded_frames[i] = (encoded_frames[i] & ~(1 << j)) | (int(binary_message[message_index]) << j)
                message_index += 1

    # Save the encoded audio file
    encoded_audio = wave.open(output_file, 'wb')
    encoded_audio.setparams(params)
    encoded_audio.writeframes(encoded_frames)
    encoded_audio.close()

def decode_audio(file_path):
    # Open the encoded audio file
    encoded_audio = wave.open(file_path, 'rb')
    frames = encoded_audio.readframes(encoded_audio.getnframes())

    # Extract the hidden message
    binary_message = ''
    for frame in frames:
        for j in range(8):
            binary_message += str((frame >> j) & 1)

    # Find the delimiter and extract the message
    delimiter_index = binary_message.find('11111111')
    if delimiter_index == -1:
        raise Exception("No hidden message found in the audio file.")
    binary_message = binary_message[:delimiter_index]

    # Convert the binary message to text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

    return message

def main():
    parser = argparse.ArgumentParser(description='Audio Steganography')
    parser.add_argument('-e', '--encode', action='store_true', help='Encode audio file')
    parser.add_argument('-d', '--decode', action='store_true', help='Decode audio file')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input audio file')
    parser.add_argument('-o', '--output_file', type=str, help='Output audio file')
    parser.add_argument('-m', '--message', type=str, help='Secret message to hide')
    args = parser.parse_args()

    if args.encode:
        if not args.output_file or not args.message:
            parser.error("Output file and message are required for encoding.")
        encode_audio(args.input_file, args.message, args.output_file)
        print("Encoded audio file generated successfully.")
    elif args.decode:
        decoded_message = decode_audio(args.input_file)
        print("Decoded message:", decoded_message)
    else:
        parser.error("Either encode or decode option is required.")

if __name__ == "__main__":
    main()