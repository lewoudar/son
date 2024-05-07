import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import click
from nava import play
from rich.progress import Progress

from son.console import console, error_console
from son.media import get_compatible_nava_file_or_raise_error
from son.settings import Settings

if TYPE_CHECKING:
    from son.main import Container

ACTIVITY_CHOICES = ['session', 's', 'work', 'w', 'short break', 'sb', 'long break', 'lb']


@dataclass(frozen=True)
class Activity:
    name: str
    duration: int


def get_activity_information(activity_type: str, settings: Settings) -> Activity:
    if activity_type in ACTIVITY_CHOICES[2:4]:
        return Activity(ACTIVITY_CHOICES[2], settings.pomo_work_time)
    elif activity_type in ACTIVITY_CHOICES[4:6]:
        return Activity(ACTIVITY_CHOICES[4], settings.pomo_short_break_time)
    elif activity_type in ACTIVITY_CHOICES[6:8]:
        return Activity(ACTIVITY_CHOICES[6], settings.pomo_long_break_time)
    else:
        duration = (
            (settings.pomo_work_time + settings.pomo_short_break_time) * 3
            + settings.pomo_work_time
            + settings.pomo_long_break_time
        )
        return Activity('session', duration)


def show_progress(activity: str, duration: int) -> None:
    with Progress(console=console) as progress:
        task = progress.add_task(f'{activity}', total=duration)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)


def get_sound(sound: Path, settings: Settings) -> str:
    return str(settings.pomo_sound if sound is None else get_compatible_nava_file_or_raise_error(sound, settings))


def run_pomodoro_session(sound: str, long_break_interval: int, settings: Settings) -> None:
    # to align the progress indicator for all activities, I use the "ljust" string method
    # on activities "work" and "long break" to align with the "short break" activity.
    short_break_length = len('short break')
    aligned_work_indication = 'work'.ljust(short_break_length)
    for _ in range(long_break_interval - 1):
        show_progress(aligned_work_indication, settings.pomo_work_time)
        play(sound)
        console.print('[info]Well done mate! time to pause a bit. :sleeping_face:')
        show_progress('short break', settings.pomo_short_break_time)
        play(sound)
        console.print('[info]Time to get back to business! :person_lifting_weights:')
    show_progress(aligned_work_indication, settings.pomo_work_time)
    play(sound)
    console.print('[info]You can now take a long-deserved pause. :sleeping_face:')
    show_progress('long break'.ljust(short_break_length), settings.pomo_long_break_time)
    play(sound)
    console.print('[success]Congratulations! You have completed a full pomodoro session! :clapping_hands:')


@click.command()
@click.option(
    '-a',
    '--activity',
    'activity_type',
    type=click.Choice(ACTIVITY_CHOICES, case_sensitive=False),
    default='session',
    show_default=True,
    help='The pomodoro activity type. Values "session", "work", "short break", "long break" have a short option '
    'counterpart you can use: "s", "w", "sb", "lb".',
)
@click.option(
    '-d',
    '--duration',
    type=click.IntRange(min=1),
    help='The time in seconds that the pomodoro activity is run. This will override the default value configured.'
    ' Beware that it is not possible to set it for the "session" activity.',
)
@click.option(
    '-s', '--sound', type=click.Path(exists=True, dir_okay=False, path_type=Path), help='The alarm sound file to play.'
)
@click.option(
    '-l',
    '--long-break-interval',
    type=click.IntRange(min=1),
    help='The number of "work" activities before a long break if you are running a "session" activity.',
)
@click.pass_obj
def pomodoro(
    obj: 'Container',
    activity_type: str,
    duration: int | None = None,
    sound: Path | None = None,
    long_break_interval: int | None = None,
):
    """
    Starts a pomodoro activity.

    There are four types of activities you can run:

    \b
    - "work" (w) - it is a work session of 25 minutes by default unless you configure the duration.
    - "short break" (sb) - it comes after a "work" activity, it defaults to 5 minutes.
    - "long break" (lb) - it comes after 3 "work/short break" activities and defaults to 15 minutes.
    - "session" (s) - a series of 3 "work/short break" activities plus a long break. This is the default activity.

    For more information about the pomodoro technique, you can read this wikipedia page:
    https://en.wikipedia.org/wiki/Pomodoro_Technique

    Example usage:

    \b
    # starts a pomodoro session with 3 "work/short break" activities plus a "long break".
    $ son pomodoro

    \b
    # starts a pomodoro session  with 2 (instead of 3) "work/short break" activities plus a "long break".
    $ son pomodoro -l 2

    \b
    # starts a pomodoro session with a alarm sound file different than the default one.
    $ son pomodoro -s my_custom_alarm.wav

    \b
    # start a "work" pomodoro activity
    $ son pomodoro -a work
    $ son pomodoro -a w

    \b
    # start a "short break" pomodoro activity with a duration of 2 minutes instead of 5. Time is in seconds.
    $ son pomodoro -a sb -d 120
    """
    activity_type = activity_type.lower()
    if duration is not None and activity_type in ACTIVITY_CHOICES[:2]:
        error_console.print('[error] You cannot set a duration for "session" activity.')
        raise SystemExit(1)

    activity = get_activity_information(activity_type, obj.settings)
    duration = duration or activity.duration
    sound = get_sound(sound, obj.settings)
    if activity.name != 'session':
        show_progress(activity.name, duration)
        play(sound)
    else:
        long_break_interval = long_break_interval or obj.settings.pomo_long_break_interval
        run_pomodoro_session(sound, long_break_interval, obj.settings)
