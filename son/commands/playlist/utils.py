from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import questionary
from alchemical import Alchemical
from rich.table import Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from son.console import console, error_console
from son.database import Playlist, Song
from son.media import get_media_duration

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


def add_songs_to_db(db: Alchemical, playlist_id: int, songs: Iterable[Path]) -> None:
    # it is not efficient to use one transaction per song, but it is convenient to print
    # accurate error message and prevent stopping the loop for one duplicated song
    for song in songs:
        try:
            with db.begin() as session:
                song = song.resolve()
                duration = get_media_duration(song)
                session.add(Song(path=song.as_posix(), playlist_id=playlist_id, duration=duration))
        except IntegrityError:
            console.print(f':cross_mark: [warning]Song [bold]{song}[/] already exists and was not added.')
            continue
        console.print(f':heavy_check_mark:  Song [info]{song}[/] was added to playlist.')


def add_songs_and_folders(
    db: Alchemical, playlist_id: int, songs: Iterable[Path], song_folders: Iterable[Path]
) -> None:
    add_songs_to_db(db, playlist_id, songs)
    for folder in song_folders:
        add_songs_to_db(db, playlist_id, folder.rglob('*.wav'))


def positive_number_validator(value: str) -> str | bool:
    if not value.isdigit() or int(value) < 1:
        return 'You must enter a positive number'
    return True


def wav_file_validator(value: str) -> str | bool:
    path = Path(value)
    if path.is_file() and path.suffix != '.wav':
        return 'You must select a .wav file'
    return True


def add_songs_and_folders_interactively(db: Alchemical, playlist_id: int) -> None:
    song_paths = []
    folder_paths = []
    nb_of_paths_to_add = int(
        questionary.text('How many songs/folders to add?', validate=positive_number_validator, qmark='>').ask()
    )
    for _ in range(nb_of_paths_to_add):
        path = Path(questionary.path('Path to song/folder:', validate=wav_file_validator, qmark='>').ask())
        if path.is_dir():
            folder_paths.append(path)
        else:
            song_paths.append(path)
    add_songs_and_folders(db, playlist_id, song_paths, folder_paths)
