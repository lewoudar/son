from collections.abc import Iterable
from datetime import datetime
from typing import TYPE_CHECKING

from rich.table import Table
from sqlalchemy.orm import Session, selectinload

from son.console import console, error_console
from son.database import Playlist

if TYPE_CHECKING:
    pass


def get_playlist_or_raise_error(name: str, session: Session, select_songs: bool = False) -> Playlist:
    statement = Playlist.select().where(Playlist.name == name)
    if select_songs:
        statement.options(selectinload(Playlist.songs))
    playlist = session.execute(statement).scalar_one_or_none()
    if playlist is None:
        error_console.print(f'[error]There is no playlist [bold]{name}[/].')
        raise SystemExit(1)
    return playlist


def get_printable_datetime(dt: datetime | None) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S') if dt is not None else ''


def print_table(title: str, headers: tuple[str, ...], rows: Iterable[tuple[str, ...]]) -> None:
    table = Table(title=title, title_style='cyan')
    for header in headers:
        table.add_column(header, header_style='bold magenta')

    for row in rows:
        table.add_row(*row)

    console.print(table)
