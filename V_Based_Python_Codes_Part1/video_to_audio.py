from moviepy.editor import *

def convert_video_to_audio(video_file: str, audio_format: str) -> str:
    """
    Converts a video file to an audio file.

    Args:
        video_file (str): Path to the video file.
        audio_format (str): Format of the output audio file (e.g., ".mp3", ".wav", ".ogg").

    Returns:
        str: Path to the output audio file.
    """
    # Load video using moviepy
    video = VideoFileClip(video_file)

    # Extract audio
    audio = video.audio

    # Save audio
    audio_file = video_file.rsplit('.', 1)[0] + audio_format
    audio.write_audiofile(audio_file)

    return audio_file

def main():
    video_file = input("Enter the path to the video file: ")
    audio_format = input("Enter the desired audio format (e.g., .mp3, .wav, .ogg): ")

    try:
        audio_file = convert_video_to_audio(video_file, audio_format)
        print(f"Audio saved as: {audio_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()