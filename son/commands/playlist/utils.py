from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from son.console import error_console
from son.database import Playlist

if TYPE_CHECKING:
    pass


def get_playlist_or_raise_error(name: str, session: Session) -> Playlist:
    playlist = session.execute(Playlist.select().where(Playlist.name == name)).scalar_one_or_none()
    if playlist is None:
        error_console.print(f'[error]There is no playlist [bold]{name}[/].')
        raise SystemExit(1)
    return playlist
