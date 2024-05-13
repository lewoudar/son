from typing import TYPE_CHECKING

import click

from .utils import get_playlist_or_raise_error

if TYPE_CHECKING:
    from son.main import Container


@click.command()
@click.argument('name')
@click.pass_obj
def describe(obj: 'Container', name: str):
    """
    Describe a playlist.

    Arguments:
        NAME  the name of the playlist.
    """
    with obj.db.Session() as session:
        playlist = get_playlist_or_raise_error(name, session)
