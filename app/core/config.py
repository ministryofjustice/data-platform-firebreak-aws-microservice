from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    aws_account_id: str
    oidc_domain: str
    oidc_eks_provider: str
    oidc_api_audience: str
    oidc_issuer: str
    oidc_algorithms: str = "RS256"

    model_config = SettingsConfigDict(extra="allow", env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
