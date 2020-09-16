import lyricsgenius as genius

from settings import GENIUS_API_ACCESS_TOKEN

genius = genius.Genius(GENIUS_API_ACCESS_TOKEN)

def get_lyrics(song_name, artist):
    song = genius.search_song(song_name, artist=artist)
    return song.lyrics if song else None
