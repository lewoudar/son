import random
import time
from pathlib import Path
from typing import TYPE_CHECKING

import click
import nava

from son.commands.playlist.utils import get_playlist_or_raise_error
from son.console import console, show_play_progress
from son.database import Song

if TYPE_CHECKING:
    from son.main import Container


def run_playlist(songs: list[Song]) -> None:
    count = len(songs)
    for index, song in enumerate(songs, start=1):
        sound_id = nava.play(song.path, async_mode=True)
        show_play_progress(song.duration, f'[bold]{Path(song.path).name}[/] [cyan]({index}/{count})[/]', transient=True)
        nava.stop(sound_id)
        # without time, it is a bit quick between songs ^^
        time.sleep(1)

    console.print('[info]Playlist finished!')


@click.command()
@click.argument('name')
@click.option('--shuffle', is_flag=True, default=False, help='Shuffle songs in the playlist before reading them.')
@click.option('--loop', is_flag=True, default=False, help='Play the playlist in loop.')
@click.pass_obj
def play(obj: 'Container', name: str, shuffle: bool, loop: bool):
    """
    Plays the given playlist.

    \b
    Arguments:
        NAME    the name of the playlist.

    Example usage:

    \b
    # Normal play
    $ son playlist play my-playlist

    \b
    # Plays songs in random order
    $ son playlist play my-playlist --shuffle

    \b
    # Plays songs in loop
    $ son playlist play my-playlist --loop

    \b
    # You can mix options
    $ son playlist play my-playlist --shuffle --loop
    """
    with obj.db.Session() as session:
        playlist = get_playlist_or_raise_error(name, session, select_songs=True)
        existing_songs = []
        not_found_songs = []
        for song in playlist.songs:
            if Path(song.path).exists():
                existing_songs.append(song)
            else:
                not_found_songs.append(song.path)

        if not_found_songs:
            console.print('[warning]The following songs do not exist, you should remove them from playlist:')
            for song_path in not_found_songs:
                console.print(f'• {song_path}')

        if not existing_songs:
            console.print('[warning]No song found, so nothing to play. :person_shrugging:')
            return

        if shuffle:
            random.shuffle(existing_songs)

        if loop:
            while True:
                run_playlist(existing_songs)
        else:
            run_playlist(existing_songs)
