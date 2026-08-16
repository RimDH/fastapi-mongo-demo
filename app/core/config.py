from pydantic_settings import BaseSettings, SettingsConfigDict

#reads values from .env file
#.env
# ↓
#config.py
# ↓
#settings
# ↓
#application
class Settings(BaseSettings):
    mongodb_url: str
    database_name: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()