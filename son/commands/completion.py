# ruff: noqa: S602
import subprocess
from pathlib import Path

import click
import shellingham

from son.console import console, error_console

SHELLS = ['bash', 'zsh', 'fish']


def install_bash_zsh(bash: bool = True) -> None:
    home = Path.home()
    completion_dir = home / '.cli_completions'
    if bash:
        shell = 'bash'
        shell_config_file = home / '.bashrc'
    else:
        shell = 'zsh'
        shell_config_file = home / '.zshrc'

    if not completion_dir.exists():
        completion_dir.mkdir()

    try:
        command = f'_SON_COMPLETE={shell}_source son'
        result = subprocess.run(command, shell=True, capture_output=True, check=True)
    except subprocess.CalledProcessError:
        error_console.print('[error]Unable to get completion script for son cli.')
        raise SystemExit(1) from None

    completion_script = completion_dir / f'son-complete.{shell}'
    completion_script.write_text(result.stdout.decode())

    with shell_config_file.open('a') as f:
        f.write(f'\n. {completion_script.absolute()}\n')


def install_fish() -> None:
    home = Path.home()
    completion_dir = home / '.config/fish/completions'
    if not completion_dir.exists():
        completion_dir.mkdir(parents=True)

    try:
        command = '_SON_COMPLETE=fish_source son'
        result = subprocess.run(command, shell=True, capture_output=True, check=True)
    except subprocess.CalledProcessError:
        error_console.print('[error]Unable to get completion script for son cli.')
        raise SystemExit(1) from None

    completion_script = completion_dir / 'son.fish'
    completion_script.write_text(result.stdout.decode())


def _install_completion(shell: str) -> None:
    if shell == 'bash':
        install_bash_zsh()
    elif shell == 'zsh':
        install_bash_zsh(bash=False)
    else:
        install_fish()


@click.command('install-completion')
def install_completion():
    """
    Install completion script for bash, zsh and fish shells.

    You will need to restart the shell for the changes to be loaded.
    """
    try:
        shell, _ = shellingham.detect_shell()
    except shellingham.ShellDetectionFailure:
        error_console.print('[error]Unable to detect the current shell.')
        raise SystemExit(1) from None
    except RuntimeError as e:
        click.echo(f'[error]{e}')
        raise SystemExit(1) from None

    if shell not in SHELLS:
        error_console.print(f'[error]Your shell is not supported. Shells supported are: {", ".join(SHELLS)}')
        raise SystemExit(1) from None

    _install_completion(shell)
    console.print('[success]Successfully installed completion script!')
