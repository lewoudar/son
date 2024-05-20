from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

import click
import questionary

from son.console import console, error_console
from son.database import Song

from .utils import get_playlist_or_raise_error

if TYPE_CHECKING:
    from son.main import Container


def print_warning_message(songs: set[str]) -> None:
    if not songs:
        return
    console.print('[warning]The following songs were not found:')
    for song in songs:
        console.print(f'• {song}')


def print_successful_message(song_paths: Iterable[str]) -> None:
    console.print('[success]The following songs were removed:')
    for song in song_paths:
        # paths seem to be highlighted by rich, I don't want that
        console.print(f':heavy_check_mark:  {song}', highlight=False)


def handle_non_interactive_song_removal(obj: 'Container', playlist_name: str, songs: set[str]) -> None:
    if not songs:
        console.print('[warning]No songs were provided, so nothing to do. :person_shrugging:')
        return
    with obj.db.begin() as session:
        playlist = get_playlist_or_raise_error(playlist_name, session)
        song_models = session.execute(Song.select().where(Song.playlist == playlist, Song.path.in_(songs))).scalars()

        database_song_paths = {song.path for song in song_models}
        songs_not_found = songs - database_song_paths
        print_warning_message(songs_not_found)

        session.execute(Song.delete().where(Song.playlist == playlist, Song.path.in_(database_song_paths)))

    if database_song_paths:
        print_successful_message(database_song_paths)
    else:
        console.print('[info]No songs were removed.')


def handle_interactive_song_removal(obj: 'Container', playlist_name: str) -> None:
    with obj.db.begin() as session:
        playlist = get_playlist_or_raise_error(playlist_name, session, select_songs=True)
        song_paths = questionary.checkbox('Select songs to remove', [song.path for song in playlist.songs]).ask()
        if not song_paths:
            console.print('[warning]No songs were selected, so nothing to do. :person_shrugging:')
            return

        session.execute(Song.delete().where(Song.playlist == playlist, Song.path.in_(song_paths)))
        print_successful_message(song_paths)


@click.command('rm-songs')
@click.argument('name')
@click.option(
    '-s',
    '--song',
    'songs',
    callback=lambda ctx, param, value: {Path(item).as_posix() for item in value},
    multiple=True,
    help='Song to remove. You should pass the full path of the song.',
)
@click.option(
    '-i', '--interactive', is_flag=True, default=False, help='Choose songs to delete from the displayed select form.'
)
@click.pass_obj
def remove_songs(obj: 'Container', name: str, songs: set[str], interactive: bool):
    """
    Removes songs from given playlist.

    \b
    Arguments:
        NAME    The name of the playlist.
    """
    if songs and interactive:
        error_console.print('[error]You cannot use interactive mode and passed songs to remove.')
        raise SystemExit(1)

    if not interactive:
        handle_non_interactive_song_removal(obj, name, songs)
    else:
        handle_interactive_song_removal(obj, name)
