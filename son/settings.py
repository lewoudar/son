from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='son_')

    default_loop_time: float = 24 * 60 * 60  # defaults to one day in seconds
