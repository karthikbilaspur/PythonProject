import googleapiclient.discovery
from google.oauth2 import service_account
import re

# YouTube API credentials
API_KEY = ''  # Replace with your actual API key
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = ''

# Authenticate with the YouTube Data API
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

youtube = googleapiclient.discovery.build(
    'youtube', 'v3', credentials=credentials)

def extract_video_id(url):
    # Regular expression to extract video ID from YouTube URL
    patterns = [
        r"^https://www\.youtube\.com/watch\?v=([^&]+)$",
        r"^https://youtu\.be/([^&]+)$"
    ]
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_stats(video_id):
    try:
        # Retrieve live views and likes data
        request = youtube.videos().list(
            part='statistics,snippet',
            id=video_id
        )
        response = request.execute()

        # Extract live views and likes count from the API response
        if 'items' in response and len(response['items']) > 0:
            statistics = response['items'][0]['statistics']
            snippet = response['items'][0]['snippet']
            live_views = int(statistics.get('viewCount', 0))
            live_likes = int(statistics.get('likeCount', 0))
            live_comments = int(statistics.get('commentCount', 0))
            title = snippet.get('title', '')

            # Print the results
            print(f"Title: {title}")
            print(f"Live views: {live_views}")
            print(f"Live likes: {live_likes}")
            print(f"Live Comments: {live_comments}")
        else:
            print('No video statistics found')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    url = input("Enter YouTube Video Link: ")
    video_id = extract_video_id(url)
    if video_id:
        get_video_stats(video_id)
    else:
        print("Invalid YouTube video link.")

if __name__ == '__main__':
    main()