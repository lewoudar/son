from typing import TYPE_CHECKING
import time

import click
import nava

from son.media import get_media_duration

if TYPE_CHECKING:
    from son.main import Container


@click.command()
@click.argument('sound', type=click.Path(exists=True, dir_okay=False))
@click.option('--loop', is_flag=True, help='Loop the audio file.')
@click.pass_obj
def play(obj: 'Container', sound: str, loop: bool):
    """
    Run SOUND wav file passed as input.
    """
    # Unfortunately, nava doesn't play in async mode without a sleep time,
    # so we need to compute the exact time the sound will take to play and pause that exact time
    # if the user wants to play in loop, we consider the default_loop_time setting value instead
    settings = obj.settings
    sound_id = nava.play(sound, async_mode=True, loop=loop)
    sleep_time = settings.default_loop_time if loop else get_media_duration(sound)
    time.sleep(sleep_time)
    nava.stop(sound_id)
