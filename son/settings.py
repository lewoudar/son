from pathlib import Path

from pydantic import Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_default_alarm_sound() -> Path:
    return Path(__file__).parent / 'sounds' / 'alarm.wav'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='son_')
    auto_conversion: bool = False
    pomo_sound: FilePath = Field(default_factory=get_default_alarm_sound)
    pomo_work_time: int = Field(default=25 * 60, description='Work time in seconds')
    pomo_short_break_time: int = Field(default=5 * 60, description='Short break time in seconds')
    pomo_long_break_time: int = Field(default=15 * 60, description='Long break time in seconds')
    pomo_long_break_interval: int = Field(default=4, description='Number of work sessions before a long break')
