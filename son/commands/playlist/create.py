from pathlib import Path
from typing import TYPE_CHECKING

import click
from alchemical import Alchemical
from sqlalchemy.exc import IntegrityError

from son.commands.playlist.utils import add_songs_and_folders, add_songs_and_folders_interactively
from son.console import console, error_console
from son.database import Playlist

if TYPE_CHECKING:
    from son.main import Container


def create_playlist(name: str, db: Alchemical) -> int:
    try:
        with db.begin() as session:
            playlist = Playlist(name=name)
            session.add(playlist)
            session.flush()
            return playlist.id
    except IntegrityError:
        error_console.print(f'[error]Playlist [bold]{name}[/] already exists.')
        raise SystemExit(1) from None


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
def create(obj: 'Container', name: str, songs: tuple[Path], song_folders: tuple[Path], interactive: bool):
    """
    Creates a playlist with songs passed as input.

    \b
    Arguments:
        NAME    the name of the playlist.

    Example Usage:

    \b
    # create a playlist with two songs
    $ son playlist create my-playlist -s song1.wav -s song2.wav

    \b
    # create a playlist with songs coming from a folder
    $ son playlist create my-playlist -f song_folder

    \b
    # You can combine direct songs and songs from folders
    $ son playlist create my-playlist -f folder1 -f folder2 -s song1.wav -s song2.wav

    \b
    # create a playlist with songs added interactively
    $ son playlist create my-playlist -i
    """
    playlist_id = create_playlist(name, obj.db)
    console.print(f'[success]Playlist [bold]{name}[/] created. :glowing_star:')

    add_songs_and_folders(obj.db, playlist_id, songs, song_folders)
    if interactive:
        add_songs_and_folders_interactively(obj.db, playlist_id)
