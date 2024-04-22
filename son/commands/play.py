import click
import nava

from son.console import show_play_progress
from son.media import get_media_duration


@click.command()
@click.argument('sound', type=click.Path(exists=True, dir_okay=False))
@click.option('--loop', is_flag=True, help='Loop the audio file.')
def play(sound: str, loop: bool):
    """
    Run SOUND wav file passed as input.

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
    # Note: nava doesn't play in async mode without a sleep time,
    # in our case the sleep resides inside the function showing the progress bar
    sound_id = nava.play(sound, async_mode=True, loop=loop)
    sound_duration = get_media_duration(sound)
    if loop:
        while True:
            show_play_progress(sound_duration, sound, transient=True)
    else:
        show_play_progress(sound_duration, sound)
    nava.stop(sound_id)
