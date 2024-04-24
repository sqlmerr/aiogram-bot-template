from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    MONGO_URL: SecretStr = Field("mongodb://localhost:27017/")

    use_webhooks: bool = True
    WEB_SERVER_HOST: str = "127.0.0.1"
    WEB_SERVER_PORT: int = 8080
    BASE_WEBHOOK_URL: str = "https://example.com"
    WEBHOOK_SECRET: str = "my-secret"
    WEBHOOK_PATH: str = "/webhook"

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)


settings = Settings()
