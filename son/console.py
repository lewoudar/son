import math
import time
from pathlib import Path

from rich.console import Console
from rich.progress import track
from rich.style import Style
from rich.theme import Theme

data = {
    'warning': Style(color='yellow'),
    'label': Style(color='yellow'),
    'info': Style(color='blue'),
    'success': Style(color='green'),
}
custom_theme = Theme(data)

console = Console(theme=custom_theme)
error_console = Console(theme=Theme({'error': Style(color='red')}), stderr=True)


def show_play_progress(duration: float, filename: Path, transient: bool = False) -> None:
    # a fraction of a second is not really important, we just consider the lower integer
    # value for simplicity
    duration = math.floor(duration)
    for _ in track(range(duration), total=duration, description=f'Playing {filename}', transient=transient):
        time.sleep(1)
