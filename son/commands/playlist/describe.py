from pathlib import Path
from typing import TYPE_CHECKING

import click
from rich.panel import Panel

from son.commands.playlist.utils import get_playlist_or_raise_error, get_printable_datetime, print_table
from son.console import console

if TYPE_CHECKING:
    from son.main import Container


def print_panel(title: str, fields: dict[str, str]) -> None:
    sorted_keys = sorted(fields.keys(), key=len, reverse=True)
    longest_field_length = len(sorted_keys[0])
    text_to_render = ''
    for field, value in fields.items():
        text_to_render += f'{field.ljust(longest_field_length)} : {value}\n'
    # #FFD700 => gold color (shamefully asked ChatGPT)
    console.print(Panel.fit(text_to_render, title=title, border_style='bold #FFD700'))


def get_printable_duration(duration: int) -> str:
    minutes, seconds = divmod(duration, 60)
    # Calculate hours and minutes
    hours, minutes = divmod(minutes, 60)

    # Generate formatted time string
    time_str = ''
    if hours > 0:
        time_str += f'{hours}h'
    if minutes > 0:
        time_str += f'{minutes}m'
    if seconds > 0:
        time_str += f'{seconds}s'
    return time_str


@click.command()
@click.argument('name')
@click.pass_obj
def describe(obj: 'Container', name: str):
    """
    Describes a playlist.

    \b
    Arguments:
        NAME    the name of the playlist.

    Example usage:

    $ son playlist describe my-playlist
    """
    with obj.db.Session() as session:
        playlist = get_playlist_or_raise_error(name, session, select_songs=True)
        fields = {
            'creation date': get_printable_datetime(playlist.created_at),
            'last update': get_printable_datetime(playlist.updated_at),
        }
        print_panel(name, fields)

        rows = []
        for song in playlist.songs:
            song_path = Path(song.path)
            rows.append(
                (
                    song_path.stem,
                    song.path,
                    get_printable_datetime(song.created_at),
                    get_printable_duration(song.duration),
                )
            )

        print_table('Songs', ('title', 'path', 'creation date', 'duration'), rows)
