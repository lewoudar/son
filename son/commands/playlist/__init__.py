import click
from .create import create
from .list import list_playlists
from .delete import delete
from .clear import clear
from .describe import describe


@click.group()
def playlist():
    """
    Manages audio playlists.
    """


for command in [create, list_playlists, delete, clear, describe]:
    playlist.add_command(command)
