import time

from rich.console import Console
from rich.progress import Progress
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


def show_play_progress(duration: int, message: str, transient: bool = False) -> None:
    with Progress(console=console, transient=transient) as progress:
        task = progress.add_task(f'[info]Playing {message}', total=duration)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)
