from pathlib import Path
import click

from son.media import convert_to_wav
from son.console import console


@click.command('to-wav')
@click.argument('audio_file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    '-o', '--output-file', type=click.Path(dir_okay=False, writable=True, path_type=Path), help='The wav output file.'
)
def to_wav(audio_file: Path, output_file: Path):
    """
    Converts AUDIO_FILE to wav format.

    \b
    Arguments:
    AUDIO_FILE      an audio file to convert in wav format.
    """
    output_path = convert_to_wav(audio_file, output_file)
    console.print(f'[success]Wav file [italic bold]{output_path}[/] was successfully created!')
