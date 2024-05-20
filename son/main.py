import click
import platformdirs
from alchemical import Alchemical
from click_didyoumean import DYMGroup

from son.commands.completion import install_completion
from son.commands.play import play
from son.commands.playlist import playlist
from son.commands.pomodoro import pomodoro
from son.commands.to_wav import to_wav
from son.console import console
from son.settings import Settings


class Container:
    def __init__(self):
        self.settings = Settings()
        son_data_dir = platformdirs.user_data_path(appname='son')
        db_path = son_data_dir / 'son.db'
        self.db = Alchemical(f'sqlite:///{db_path}')
        if not son_data_dir.exists():
            son_data_dir.mkdir(parents=True, exist_ok=True)
            console.print(f'[info]Initializing database at {db_path}')
            self.db.create_all()


@click.version_option('0.1.0', message='%(prog)s version %(version)s')
@click.group(cls=DYMGroup, context_settings={'help_option_names': ['-h', '--help']})
@click.pass_context
def cli(context: click.Context):
    """
    An audio player capable of:

    \b
    - creating/managing playlists
    - manage your work time with pomodoro

    Example usage:

    \b
    # play a song
    $ son play audio.wav

    \b
    # create a new playlist
    $ son playlist create -n "my playlist" -s "sound_1.wav" -s "sound_2.wav"

    \b
    # add songs to a playlist
    $ son playlist add-songs "my playlist" -s "sound_3.wav" -s "sound_2.wav"

    \b
    # start a pomodoro session
    $ son pomodoro
    """
    context.obj = Container()


for command in [install_completion, play, to_wav, pomodoro, playlist]:
    cli.add_command(command)
