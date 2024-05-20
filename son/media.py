# ruff: noqa: S603, S607
import platform
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from son.console import console, error_console
from son.settings import Settings


def get_seconds_from_str_time(str_time: str) -> float:
    """Converts a string time in format hh:mm:ss.ss into seconds"""
    time_format = datetime.strptime(str_time, '%H:%M:%S.%f')
    delta = timedelta(
        hours=time_format.hour,
        minutes=time_format.minute,
        seconds=time_format.second,
        microseconds=time_format.microsecond,
    )
    return delta.total_seconds()


def get_media_duration(audio_file: Path) -> float:
    result = subprocess.run(['ffmpeg', '-i', audio_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode()
    matches = re.search(r'Duration: (\d{2}:\d{2}:\d{2}.\d{2})', output)
    if matches:
        return get_seconds_from_str_time(matches.group(1))

    error_console.print(f'[error]Unable not parse duration for file: [bold]{audio_file}[/], ffmpeg output\n: {output}')
    raise SystemExit(1)


def convert_to_wav(audio_file: Path, output_file: Path | None = None) -> Path:
    output_path = output_file if output_file else audio_file.with_suffix('.wav')
    console.print(f'[info]Creating [bold]{output_path}[/] from [bold]{audio_file}[/]...')
    try:
        subprocess.run(
            ['ffmpeg', '-i', audio_file, output_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True
        )
    except subprocess.CalledProcessError as e:
        error_console.print(f'[error]Unable to convert [bold]{audio_file}[/], ffmpeg error:\n {e.stdout.decode()}')
        raise SystemExit(1) from None
    return output_path


def is_nava_compatible(audio_file: Path) -> bool:
    if audio_file.suffix == '.wav' or (audio_file.suffix == '.mp3' and platform.platform() == 'Darwin'):
        return True
    return False


def get_compatible_nava_file_or_raise_error(audio_file: Path, settings: Settings) -> Path:
    if is_nava_compatible(audio_file):
        return audio_file

    if not settings.auto_conversion:
        error_console.print(
            f'[error]File extension ({audio_file.suffix}) is not supported and "auto_conversion" setting is not'
            ' activated.\n You may want to convert the audio first with the [bold]to-wav[/] command.'
        )
        raise SystemExit(1) from None
    return convert_to_wav(audio_file)
