import lyricsgenius as lg

def get_lyrics(genius, artists, max_songs):
    for artist in artists:
        try:
            songs = genius.search_artist(artist, max_songs=max_songs, sort='popularity').songs
            yield artist, songs
        except Exception as e:
            print(f"Error fetching lyrics for {artist}: {e}")

def save_lyrics(filename, songs):
    with open(filename, 'w') as file:
        for artist, songs in songs:
            file.write(f"# {artist}\n")
            for song in songs:
                file.write(song.lyrics + "\n\n")
            file.write("\n")

def main():
    filename = input("Enter a filename: ") or 'Lyrics.txt'
    genius = lg.Genius('Client_Access_Token_Goes_Here')
    genius.skip_non_songs = True
    genius.excluded_terms = ["(Remix)", "(Live)"]
    genius.remove_section_headers = True

    input_string = input("Enter name of Artists separated by spaces: ")
    artists = input_string.split()
    max_songs = 3

    songs = get_lyrics(genius, artists, max_songs)
    save_lyrics(filename, songs)

    print("Lyrics saved to", filename)

if __name__ == "__main__":
    main()