import click
from click_didyoumean import DYMGroup

from son.commands.completion import install_completion
from son.commands.play import play
from son.commands.to_wav import to_wav
from son.settings import Settings


class Container:
    def __init__(self):
        self.settings = Settings()


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
    # update a playlist
    $ son playlist update -n "my playlist" -a "sound_3.wav" -d "sound_2.wav"

    \b
    # start a pomodoro session
    $ son pomodoro start
    """
    context.obj = Container()


for command in [install_completion, play, to_wav]:
    cli.add_command(command)
