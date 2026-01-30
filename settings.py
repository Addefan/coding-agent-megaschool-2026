from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

COMMON_CONFIG = {
    "env_file": ".env",
    "extra": "ignore",
}


class ModelSettings(BaseSettings):
    base_url: str = "https://openrouter.ai/api/v1"
    api_key: str
    id: str

    model_config = SettingsConfigDict(
        **COMMON_CONFIG,
        env_prefix="MODEL_",
    )


class GithubSettings(BaseSettings):
    token: str

    model_config = SettingsConfigDict(
        **COMMON_CONFIG,
        env_prefix="GITHUB_",
    )


class Settings(BaseSettings):
    model: ModelSettings = Field(default_factory=ModelSettings)
    github: GithubSettings = Field(default_factory=GithubSettings)
    debug: bool = False

    model_config = SettingsConfigDict(**COMMON_CONFIG)


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
