from pytube import YouTube
import os

def download_video(url: str):
    yt = YouTube(url)
    print(f"Title: {yt.title}")
    print(f"Views: {yt.views}")
    print(f"Length: {yt.length} seconds")

    # Show available streams
    for i, stream in enumerate(yt.streams):
        print(f"{i+1}. {stream}")

    # Ask user for stream selection
    stream_index = int(input("Enter the stream number: ")) - 1

    # Ask user for download location
    download_location = input("Enter download location (default: current directory): ")
    if download_location.strip() == "":
        download_location = os.getcwd()

    # Download the video
    yt.streams[stream_index].download(download_location)
    print(f"Video downloaded successfully to {download_location}!")

def download_audio(url: str):
    yt = YouTube(url)
    print(f"Title: {yt.title}")
    print(f"Views: {yt.views}")
    print(f"Length: {yt.length} seconds")

    # Download audio only
    stream = yt.streams.filter(only_audio=True).first()
    download_location = input("Enter download location (default: current directory): ")
    if download_location.strip() == "":
        download_location = os.getcwd()
    stream.download(download_location)
    print(f"Audio downloaded successfully to {download_location}!")

def get_video_info(url: str):
    yt = YouTube(url)
    print(f"Title: {yt.title}")
    print(f"Views: {yt.views}")
    print(f"Length: {yt.length} seconds")
    print(f"Description: {yt.description}")
    print(f"Author: {yt.author}")
    print(f"Published: {yt.publish_date}")

def main():
    while True:
        print("\nYouTube Video Downloader")
        print("1. Download Video")
        print("2. Download Audio")
        print("3. Get Video Info")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            url = input("Enter the YouTube video URL: ")
            download_video(url)
        elif choice == "2":
            url = input("Enter the YouTube video URL: ")
            download_audio(url)
        elif choice == "3":
            url = input("Enter the YouTube video URL: ")
            get_video_info(url)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()