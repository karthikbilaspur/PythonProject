import librosa
import soundfile as sf
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import collections
import contextlib
import sys
import wave
import webrtcvad

def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate

def write_wave(path, audio, sample_rate):
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)

class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

def frame_generator(frame_duration_ms, audio, sample_rate):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n

def vad_collector(sample_rate, frame_duration_ms, padding_duration_ms, vad, frames):
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    triggered = False
    voiced_frames = []
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                triggered = False
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                voiced_frames = []
    if triggered:
        pass
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])

def split_audio_on_silence(file_path, output_dir):
    audio = AudioSegment.from_file(file_path)
    chunks = split_on_silence(
        audio,
        min_silence_len=500,
        silence_thresh=-40,
        keep_silence=100
    )
    for i, chunk in enumerate(chunks):
        chunk.export(os.path.join(output_dir, f"chunk_{i}.wav"), format="wav")

def split_audio_using_vad(file_path, output_dir):
    audio, sample_rate = read_wave(file_path)
    vad = webrtcvad.Vad(2)
    frames = frame_generator(30, audio, sample_rate)
    segments = vad_collector(sample_rate, 30, 300, vad, frames)
    for i, segment in enumerate(segments):
        path = os.path.join(output_dir, f"chunk_{i+1}.wav")
        write_wave(path, segment, sample_rate)

def main():
    print("Audio Splitting Program")
    print("1. Split audio on silence")
    print("2. Split audio using VAD")
    choice = input("Enter your choice: ")
    file_path = input("Enter the audio file path: ")
    output_dir = input("Enter the output directory path: ")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if choice == "1":
        split_audio_on_silence(file_path, output_dir)
    elif choice == "2":
        split_audio_using_vad(file_path, output_dir)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()