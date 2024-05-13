from typing import TYPE_CHECKING

import click

from son.console import console
from son.database import Playlist, Song

if TYPE_CHECKING:
    from son.main import Container


@click.command()
@click.pass_obj
def clear(obj: 'Container'):
    """Clear the playlist database."""
    with obj.db.begin() as session:
        session.execute(Playlist.delete())
        session.execute(Song.delete())

    console.print('[success]Database cleared.')
