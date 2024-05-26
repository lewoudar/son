from typing import TYPE_CHECKING

import click
from sqlalchemy.exc import IntegrityError

from son.commands.playlist.utils import get_playlist_or_raise_error
from son.console import console, error_console
from son.database import Playlist

if TYPE_CHECKING:
    from son.main import Container


@click.command('rename')
@click.argument('old_name')
@click.argument('new_name')
@click.pass_obj
def rename(obj: 'Container', old_name: str, new_name: str):
    """
    Renames a playlist.

    \b
    Arguments:
        OLD_NAME    the old name of the playlist.
        NEW_NAME    the new name of the playlist.

    Example usage:

    \b
    # Renames playlist from acoustic to RnB
    $ son playlist rename acoustic RnB
    """
    with obj.db.begin() as session:
        get_playlist_or_raise_error(old_name, session)
        try:
            session.execute(Playlist.update().where(Playlist.name == old_name).values(name=new_name))
        except IntegrityError:
            error_console.print(f'[error]Playlist [bold]{old_name}[/] already exists.')
            raise SystemExit(1) from None

        console.print(f'[success]Renamed playlist [bold]{old_name}[/] to [bold]{new_name}[/]. :glowing_star:')
