from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    oidc_domain: str
    oidc_eks_provider: str

    model_config = SettingsConfigDict(extra="allow", env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
