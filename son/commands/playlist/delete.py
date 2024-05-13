from typing import TYPE_CHECKING

import click

from son.console import console
from son.commands.playlist.utils import get_playlist_or_raise_error

if TYPE_CHECKING:
    from son.main import Container


@click.command()
@click.argument('name')
@click.pass_obj
def delete(obj: 'Container', name: str):
    """
    Deletes a playlist.

    \b
    Arguments:
        NAME   the name of the playlist.

    Example Usage:

    $ son playlist delete my-playlist
    """
    with obj.db.begin() as session:
        playlist = get_playlist_or_raise_error(name, session)
        session.delete(playlist)

    console.print(f'[success]Playlist [bold]{name}[/] deleted.')
