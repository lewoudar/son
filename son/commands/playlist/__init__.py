import click

from .clear import clear
from .create import create
from .delete import delete
from .describe import describe
from .list import list_playlists
from .remove_songs import remove_songs


@click.group()
def playlist():
    """
    Manages audio playlists.
    """


for command in [create, list_playlists, delete, clear, describe, remove_songs]:
    playlist.add_command(command)
