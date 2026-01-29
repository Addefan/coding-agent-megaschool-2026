from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

COMMON_CONFIG = {
    "env_file": ".env",
    "extra": "ignore",
}


class OpenRouterSettings(BaseSettings):
    base_url: str
    api_key: str
    model: str

    model_config = SettingsConfigDict(
        **COMMON_CONFIG,
        env_prefix="OPENROUTER_",
    )


class Settings(BaseSettings):
    openrouter: OpenRouterSettings = Field(default_factory=OpenRouterSettings)
    debug: bool = False

    model_config = SettingsConfigDict(**COMMON_CONFIG)


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
