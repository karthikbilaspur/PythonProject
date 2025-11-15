import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

# Create a Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_by_artist(artist_name: str, song_name: str) -> dict | None:
    try:
        results = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track')
        if results['tracks']['items']:
            return results['tracks']['items'][0]
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_songs_by_artist(artist_name: str) -> list[dict]:
    try:
        results = sp.search(q=f' artist:{artist_name}', type='track')
        if results['tracks']['items']:
            return results['tracks']['items']
        else:
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_songs_from_album(album_name: str) -> list[dict]:
    try:
        results = sp.search(q=f'album:{album_name}', type='album')
        if results['albums']['items']:
            album_id = results['albums']['items'][0]['id']
            album_tracks = sp.album_tracks(album_id)
            return album_tracks['items']
        else:
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def print_song_info(song: dict):
    print(f"Song: {song['name']}")
    print(f"Artist: {song['artists'][0]['name']}")
    print(f"Album: {song['album']['name']}")
    print(f"Preview URL: {song['preview_url']}")
    print()

def main():
    while True:
        print("1. Search for a song by artist")
        print("2. Get songs by an artist")
        print("3. Get songs from an album")
        print("4. Quit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            artist_name = input("Enter the artist name: ")
            song_name = input("Enter the song name: ")
            song = get_song_by_artist(artist_name, song_name)
            if song:
                print_song_info(song)
            else:
                print("Song not found")
        elif choice == '2':
            artist_name = input("Enter the artist name: ")
            songs = get_songs_by_artist(artist_name)
            if songs:
                for song in songs:
                    print_song_info(song)
            else:
                print("No songs found")
        elif choice == '3':
            album_name = input("Enter the album name: ")
            songs = get_songs_from_album(album_name)
            if songs:
                for song in songs:
                    print_song_info(song)
            else:
                print("No songs found")
        elif choice == '4':
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main()