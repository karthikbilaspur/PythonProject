"""
audio-to-spectrogram.py - Convert audio file to spectrogram image.
Can run standalone.
"""
import argparse
import pathlib
from typing import Any, Callable, cast


def audio_to_spectrogram(
    file_path: str,
    output_file: str = "spectrogram.png",
    window_size: int = 2048,
    hop_length: int = 512,
    colormap: str = "inferno",
) -> None:
    try:
        import librosa  # type: ignore[import-not-found]
        import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    except ImportError as e:
        raise ImportError(f"Missing dependency: {e}. Install from requirements.txt") from e

    librosa = cast(Any, librosa)
    plt = cast(Any, plt)

    input_path = pathlib.Path(file_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    print(f"[*] Loading audio: {file_path}")
    load_audio = cast(Callable[[str], tuple[Any, int]], librosa.load)
    audio, sr = load_audio(str(input_path))
    print(f"[*] Audio loaded at {sr} Hz")

    print(f"[*] Computing STFT (n_fft={window_size}, hop={hop_length})...")
    stft = librosa.stft(audio, n_fft=window_size, hop_length=hop_length)
    db: Any = librosa.amplitude_to_db(abs(stft), ref=max)

    plt.figure(figsize=(12, 6))
    img = plt.imshow(db, cmap=colormap, interpolation="nearest", aspect="auto", origin="lower")
    plt.title(f"Spectrogram - {input_path.name}", fontsize=14, fontweight="bold")
    plt.xlabel("Time Frames")
    plt.ylabel("Frequency Bins")
    plt.colorbar(img, format="%+2.0f dB")
    plt.tight_layout()

    output_path = pathlib.Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(str(output_path), bbox_inches="tight", dpi=200)
    print(f"[+] Spectrogram saved: {output_path}")
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Audio to Spectrogram Converter")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input audio file (wav, mp3)')
    parser.add_argument('-o', '--output', type=str, default='spectrogram.png', help='Output image file')
    parser.add_argument('-w', '--window_size', type=int, default=2048, help='Window size for STFT')
    parser.add_argument('-l', '--hop_length', type=int, default=512, help='Hop length for STFT')
    parser.add_argument('-c', '--colormap', type=str, default='inferno', help='Matplotlib colormap (hot, viridis, inferno, etc.)')
    args = parser.parse_args()

    audio_to_spectrogram(args.input, args.output, args.window_size, args.hop_length, args.colormap)

if __name__ == "__main__":
    main()
