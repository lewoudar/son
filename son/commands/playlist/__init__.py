import click

from .clear import clear
from .create import create
from .delete import delete
from .describe import describe
from .list import list_playlists
from .remove_songs import remove_songs
from .rename import rename


@click.group()
def playlist():
    """
    Manages audio playlists.
    """


for command in [create, list_playlists, delete, clear, describe, rename, remove_songs]:
    playlist.add_command(command)
