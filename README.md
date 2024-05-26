# Son

Son (sound in French) is a command line interface to play... sounds in the terminal. You can

- play sounds in **wav** format. Son can convert other audio formats if you have [ffmpeg](https://ffmpeg.org/)
  installed.
- Handle playlists.
- organize your work with the [pomodoro](https://en.wikipedia.org/wiki/Technique_Pomodoro) technique.

## Installation

You will need **Python 3.11** or higher to use son. The best way to install it is
with [pipx](https://pipx.pypa.io/stable/). You will also need to have [ffmpeg](https://ffmpeg.org/) installed on your
computer.

```shell
$ pipx install git+https://github.com/lewoudar/son
```

## Configuration

There are a few environment variables you can tweak to configure the behaviour of the _son_ command line.

- `SON_AUTO_CONVERSION`: This is related to the `son play` command. It helps to automatically converts a non `wav` file
  to the `wav` format. It defaults to **false**. The values `true`, `yes`, `on` mean **true** and the
  values `false`, `no`, `off` mean **false**.
- `SON_POMO_SOUND`: It overrides the alarm used for the command `son pomodoro`. It should be a valid file path. If the
  file is not a `wav` one and the environment variable `SON_AUTO_CONVERSION` is set to **true**, a copy with the `wav`
  extension will be created, otherwise, you will **get an error**.
- `SON_POMO_WORK_TIME`: It controls the time in **seconds** for a pomodoro work session. Defaults **1500** (25 minutes).
- `SON_POMO_SHORT_BREAK_TIME`: It controls the time in **seconds** for a pomodoro short break. Defaults to **300** (5
  minutes).
- `SON_POMO_LONG_BREAK_TIME`: It controls the time in **seconds** for a pomodoro long break. Defaults to **900** (15
  minutes).
- `SON_POMO_LONG_BREAK_INTERVAL`: It controls the number of pomodoro work sessions before taking a long break. Defaults
  to **4**.

## Usage

Normally, the command line interface is well detailed and you will not need additional documentation.

```shell
$ son -h
Usage: son.cmd [OPTIONS] COMMAND [ARGS]...

  An audio player capable of:

  - playing sounds
  - managing playlists
  - managing your work time with pomodoro

  Example usage:

  # play a song
  $ son play audio.wav

  # create a new playlist
  $ son playlist create -n "my playlist" -s "sound_1.wav" -s "sound_2.wav"

  # add songs to a playlist
  $ son playlist add-songs "my playlist" -s "sound_3.wav" -s "sound_2.wav"

  # start a pomodoro session
  $ son pomodoro

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  install-completion  Install completion script for bash, zsh and fish...
  play                Plays SOUND wav file passed as input.
  playlist            Manages audio playlists.
  pomodoro            Starts a pomodoro activity.
  to-wav              Converts AUDIO_FILE to wav format.
```

Each command is well documented.

The first command you probably want to run is `install-completion`. This will install a completion script
for `bash`, `zsh` and `fish` shells.

## Notes and warnings

There is probably room for improvements like any other application, but I don't think I will have the time/motivation
to continue it. This is why I didn't publish the project on [PyPI](https://pypi.org/). The original idea was to play
around
[nava](https://github.com/openscilab/nava), a fantastic Python project to play sounds in the terminal.

You are still encourage to fill issues if you found a critical bug. I will take time to respond, but I will definitely
check them.

But if you want to add new features, you are encourage to fork the project and makes it yours :)

There is a probably a room for a [Textual](https://textual.textualize.io/) application, but I'm too lazy to do it. If you make such an application, let me
know so that I can have a look at it :)