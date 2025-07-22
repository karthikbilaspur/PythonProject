import librosa
import matplotlib.pyplot as plt
import numpy as np
import argparse

def audio_to_spectrogram(file_path, output_file, window_size, hop_length, colormap):
    # Load audio file
    audio, sr = librosa.load(file_path)

    # Compute spectrogram
    X = librosa.stft(audio, n_fft=window_size, hop_length=hop_length)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(10, 5))
    plt.imshow(Xdb, cmap=colormap, interpolation='nearest', aspect='auto', origin='lower')
    plt.title('Spectrogram')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.colorbar()

    # Save spectrogram to file
    plt.savefig(output_file, bbox_inches='tight')

    # Display spectrogram
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Audio to Spectrogram Converter')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input audio file')
    parser.add_argument('-o', '--output_file', type=str, default='spectrogram.png', help='Output spectrogram file')
    parser.add_argument('-w', '--window_size', type=int, default=2048, help='Window size for STFT')
    parser.add_argument('-l', '--hop_length', type=int, default=512, help='Hop length for STFT')
    parser.add_argument('-c', '--colormap', type=str, default='hot', help='Colormap for spectrogram')
    args = parser.parse_args()

    audio_to_spectrogram(args.input_file, args.output_file, args.window_size, args.hop_length, args.colormap)

if __name__ == "__main__":
    main()