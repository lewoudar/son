from datetime import datetime
from typing import TYPE_CHECKING, Iterable

import click
from rapidfuzz import process, fuzz, utils
from rich.table import Table

from son.console import console
from son.database import Playlist

if TYPE_CHECKING:
    from son.main import Container


def print_table(title: str, headers: tuple[str, ...], rows: Iterable[tuple[str, ...]]) -> None:
    table = Table(title=title, title_style='cyan')
    for header in headers:
        table.add_column(header, header_style='bold magenta')

    for row in rows:
        table.add_row(*row)

    console.print(table)


def get_printable_datetime(dt: datetime | None) -> str:
    return dt.isoformat() if dt is not None else ''


@click.command('list')
@click.option('-n', '--name', help='A name used to filter playlists by performing a fuzzy search.')
@click.option(
    '-c',
    '--count',
    type=int,
    default=10,
    show_default=True,
    help='A value used in combination with  the --name option to control the number of results to return.',
)
@click.pass_obj
def list_playlists(obj: 'Container', name: str, count: int):
    """
    Lists playlists.

    Example Usage:

    $ son playlist list

    \b
    # filter playlists by name.
    $ son playlist list my-playlist -n name

    # Since the search is a fuzzy one, you can limit the number of playlists returned, by default it is 10.
    $ son playlist list my-playlist -n name -c 5
    """
    names_to_search = []
    playlists_info = {}

    with obj.db.Session() as session:
        for playlist in session.execute(Playlist.select()).scalars():
            names_to_search.append(playlist.name)
            playlists_info[playlist.name] = (
                playlist.name,
                get_printable_datetime(playlist.created_at),
                get_printable_datetime(playlist.updated_at),
            )
    if name:
        # I use "name.lower()" because the utils.default_process will "lower" the choices, so I think
        # it will be more accurate
        results = process.extract(  # type: ignore
            name.lower(), names_to_search, scorer=fuzz.WRatio, limit=count, processor=utils.default_process
        )
        rows = (playlists_info[playlist_name] for playlist_name, score, index in results)
    else:
        rows = (row for row in playlists_info.values())
    print_table('Playlists', ('name', 'created_at', 'updated_at'), rows)
