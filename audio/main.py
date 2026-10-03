"""
main.py - Orchestrator for audio_convertor project
Runs all 3 tools individually or as a combined pipeline.
"""
import argparse
import pathlib

from audio_steganography import decode_audio, encode_audio
from audio_to_spectrogram import audio_to_spectrogram
from audio_to_text import transcribe_cli

def run_full_pipeline(input_wav: str, secret_message: str, output_dir: str = "output"):
    """
    Combined pipeline:
    1. Hide message in audio -> encoded.wav
    2. Generate spectrogram of encoded audio
    3. Decode message to verify
    4. Try transcription
    """
    out_path = pathlib.Path(output_dir)
    out_path.mkdir(exist_ok=True)

    encoded_path = out_path / "encoded_with_secret.wav"
    spectrogram_path = out_path / "spectrogram_encoded.png"
    original_spec_path = out_path / "spectrogram_original.png"

    print("\n=== AUDIO CONVERTOR FULL PIPELINE ===\n")

    # Step 1: Encode
    print("[1/4] Encoding secret message...")
    encode_audio(input_wav, secret_message, str(encoded_path))

    # Step 2: Spectrogram of original
    print("\n[2/4] Generating spectrogram for original...")
    audio_to_spectrogram(input_wav, str(original_spec_path))

    # Step 3: Spectrogram of encoded
    print("\n[3/4] Generating spectrogram for encoded file...")
    audio_to_spectrogram(str(encoded_path), str(spectrogram_path))

    # Step 4: Decode and verify
    print("\n[4/4] Decoding to verify...")
    decoded = decode_audio(str(encoded_path))
    print(f"Original message : {secret_message}")
    print(f"Decoded message  : {decoded}")
    print(f"Match: {decoded == secret_message}")

    # Optional: transcription
    print("\n[*] Trying transcription (may fail if audio is not speech)...")
    try:
        transcribe_cli(input_wav)
    except Exception as e:
        print(f"Transcription skipped: {e}")

    print(f"\n[+] Pipeline complete. Files in: {out_path.resolve()}")

def main():
    parser = argparse.ArgumentParser(
        description="audio_convertor - All-in-one audio toolkit",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python main.py --stego-encode -i input.wav -o encoded.wav -m "hello"
  python main.py --stego-decode -i encoded.wav
  python main.py --to-text -i speech.wav
  python main.py --to-spectrogram -i song.wav -o spec.png
  python main.py --pipeline -i input.wav -m "secret message"
        """
    )
    parser.add_argument('--stego-encode', action='store_true', help='Run only steganography encode')
    parser.add_argument('--stego-decode', action='store_true', help='Run only steganography decode')
    parser.add_argument('--to-text', action='store_true', help='Run only audio-to-text')
    parser.add_argument('--to-spectrogram', action='store_true', help='Run only spectrogram generator')
    parser.add_argument('--pipeline', action='store_true', help='Run full combined pipeline')

    parser.add_argument('-i', '--input', type=str, help='Input audio file')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    parser.add_argument('-m', '--message', type=str, help='Secret message for steganography')

    args = parser.parse_args()

    if args.stego_encode:
        if not args.input or not args.output or not args.message:
            parser.error("--stego-encode needs -i, -o, -m")
        encode_audio(args.input, args.message, args.output)
    elif args.stego_decode:
        if not args.input:
            parser.error("--stego-decode needs -i")
        print(decode_audio(args.input))
    elif args.to_text:
        if not args.input:
            parser.error("--to-text needs -i")
        transcribe_cli(args.input)
    elif args.to_spectrogram:
        if not args.input:
            parser.error("--to-spectrogram needs -i")
        out = args.output or "spectrogram.png"
        audio_to_spectrogram(args.input, out)
    elif args.pipeline:
        if not args.input or not args.message:
            parser.error("--pipeline needs -i and -m")
        run_full_pipeline(args.input, args.message)
    else:
        parser.print_help()
        print("\nNo mode selected. Launching interactive menu...")
        interactive_menu()

def interactive_menu():
    while True:
        print("\n--- audio_convertor MENU ---")
        print("1. Steganography Encode")
        print("2. Steganography Decode")
        print("3. Audio to Text (Speech Recognition)")
        print("4. Audio to Spectrogram")
        print("5. Run FULL Pipeline (Encode + Spectrogram + Decode)")
        print("6. Quit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            inp = input("Input WAV: ").strip()
            out = input("Output WAV: ").strip()
            msg = input("Secret message: ").strip()
            encode_audio(inp, msg, out)
        elif choice == "2":
            inp = input("Encoded WAV: ").strip()
            print("Decoded:", decode_audio(inp))
        elif choice == "3":
            inp = input("Speech WAV: ").strip()
            try:
                transcribe_cli(inp)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "4":
            inp = input("Input audio: ").strip()
            out = input("Output image [spectrogram.png]: ").strip() or "spectrogram.png"
            audio_to_spectrogram(inp, out)
        elif choice == "5":
            inp = input("Input WAV: ").strip()
            msg = input("Secret message: ").strip()
            run_full_pipeline(inp, msg)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
