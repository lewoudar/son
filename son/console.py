from rich.console import Console
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
