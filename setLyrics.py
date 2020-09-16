import argparse
import os
from bs4 import element
from mutagen.id3 import ID3, USLT

from getLyrics import get_lyrics

TITLE = 'TIT2'
ARTIST = 'TPE1'
ALBUM = 'TALB'
YEAR = 'TDRC'
LYRICS = 'USLT'


def set_lyrics_to_one_song(song_tags, lyrics):
    lyrics_tag = get_lyrics_tag_name(song_tags)
    if lyrics_tag is None:
        lyrics_tag = 'USLT:desc:eng'
    song_tags[lyrics_tag] = USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics)
    song_tags.save()


def set_lyrics(songs_path, force=False):
    for song_path in songs_path:
        song_tags = ID3(song_path)
        title = song_tags[TITLE]
        artist = song_tags[ARTIST]
        lyrics_tag = get_lyrics_tag_name(song_tags)
        if not song_tags[lyrics_tag] or force:
            lyrics = get_lyrics(title, artist)
            if lyrics:
                print('Setting lyrics...')
                set_lyrics_to_one_song(song_tags, lyrics)
                print('Done!')


def get_lyrics_tag_name(song_tags):
    for tag_name in song_tags.keys():
        if 'USLT' in tag_name:
            return tag_name


def ismp3(path):
    return os.path.splitext(path)[-1] == '.mp3'


def flatten(element):
    if not isinstance(element, list):
        yield element
    else:
        for item in element:
            yield from flatten(item)


def get_mp3_paths(path, recursive=False):
    def map_function(path):
        ret = None
        if ismp3(path):
            return path
        elif recursive and os.path.isdir(path):
            return list(flatten(get_mp3_paths(path, recursive)))
        else:
            return []

    with os.scandir(path) as files:
        return list(flatten(list(map(map_function, files))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--recursive', action='store_true')
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('path', nargs='+')

    args = parser.parse_args()

    paths = []
    for path in args.path:
        if os.path.isdir(path):
            paths += get_mp3_paths(path, args.recursive)
        elif ismp3(path):
            paths += [path]
    
    set_lyrics(paths, force=args.force)


main()
