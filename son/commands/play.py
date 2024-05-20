from pathlib import Path
from typing import TYPE_CHECKING

import click
import nava

from son.console import show_play_progress
from son.media import get_compatible_nava_file_or_raise_error, get_media_duration

if TYPE_CHECKING:
    from son.main import Container


@click.command()
@click.argument('sound', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('--loop', is_flag=True, help='Loop the audio file.')
@click.pass_obj
def play(obj: 'Container', sound: Path, loop: bool):
    """
    Run SOUND wav file passed as input.

    If SOUND is not a wav file, a copy with the wav format will be automatically created in the same directory.

    \b
    Arguments:
        SOUND       an audio file to play.

    \b
    Example usage:
    $ son play audio.wav

    \b
    # to play in loop
    $ son play audio.wav --loop
    """
    sound = get_compatible_nava_file_or_raise_error(sound, obj.settings)
    # Note: nava doesn't play in async mode without a sleep time,
    # in our case the sleep resides inside the function showing the progress bar
    sound_id = nava.play(str(sound), async_mode=True, loop=loop)
    sound_duration = get_media_duration(sound)
    if loop:
        while True:
            show_play_progress(sound_duration, sound, transient=True)
    else:
        show_play_progress(sound_duration, sound)
    nava.stop(sound_id)
