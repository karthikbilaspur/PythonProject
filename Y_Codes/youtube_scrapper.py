from pytube import YouTube
import json

class YouTubeScrapper:
    def __init__(self, url: str):
        self.url = url
        self.yt = YouTube(self.url)

    def get_video_info(self):
        video_info = {
            "title": self.yt.title,
            "description": self.yt.description,
            "views": self.yt.views,
            "rating": self.yt.rating,
            "length": self.yt.length,
            "author": self.yt.author,
        }
        return video_info

    def get_video_streams(self):
        streams = []
        for stream in self.yt.streams:
            stream_info = {
                "itag": stream.itag,
                "mime_type": stream.mime_type,
                "resolution": stream.resolution,
                "fps": stream.fps,
                "vcodec": stream.vcodec,
                "acodec": stream.acodec,
                "progressive": stream.is_progressive,
            }
            streams.append(stream_info)
        return streams

    def download_video(self, itag: int):
        stream = self.yt.streams.get_by_itag(itag)
        if stream:
            stream.download()
            print("Video downloaded successfully.")
        else:
            print("Invalid itag.")

def main():
    url = input("Enter YouTube video URL: ")
    scrapper = YouTubeScrapper(url)
    video_info = scrapper.get_video_info()
    print(json.dumps(video_info, indent=4))
    streams = scrapper.get_video_streams()
    print(json.dumps(streams, indent=4))
    itag = input("Enter itag to download: ")
    scrapper.download_video(itag)

if __name__ == "__main__":
    main()