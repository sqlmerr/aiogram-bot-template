from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr

    echo: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
