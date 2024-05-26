from pathlib import Path
from typing import TYPE_CHECKING

import click

from son.commands.playlist.utils import (
    add_songs_and_folders,
    add_songs_and_folders_interactively,
    get_playlist_or_raise_error,
)

if TYPE_CHECKING:
    from son.main import Container


@click.command()
@click.argument('name')
@click.option(
    '-s',
    '--song',
    'songs',
    multiple=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help='Song to add to the playlist. Only "wav" files are supported.',
)
@click.option(
    '-f',
    '--folder',
    'song_folders',
    multiple=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help='Folder containing songs to add to the playlist. Only ".wav" files will be found and added.',
)
@click.option(
    '-i', '--interactive', is_flag=True, default=False, help='Choose songs to add from the file explorer input.'
)
@click.pass_obj
def add_songs(obj: 'Container', name: str, songs: tuple[Path], song_folders: tuple[Path], interactive: bool):
    """
    Adds songs to the given playlist.

    \b
    Arguments:
        NAME    The name of the playlist.

    Example usage:

    \b
    # adds two songs to the playlist my-playlist
    $ son playlist add-songs my-playlist -s song1.wav -s song2.wav

    \b
    # adds songs from the folder song_folder to the playlist my-playlist
    $ son playlist add-songs my-playlist -f song_folder

    \b
    # we can combine direct songs and songs from folders
    $ son playlist add-songs my-playlist -f folder1 -f folder2 -s song1.wav -s song2.wav

    \b
    # adds songs interactively
    $ son playlist add-songs my-playlist -i
    """
    with obj.db.Session() as session:
        playlist = get_playlist_or_raise_error(name, session)
        add_songs_and_folders(obj.db, playlist.id, songs, song_folders)

    if interactive:
        add_songs_and_folders_interactively(obj.db, playlist.id)
