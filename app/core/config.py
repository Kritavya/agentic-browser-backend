"""
Application Configuration.

Centralized configuration management using Pydantic Settings.
All configuration values should be loaded from environment variables
or .env files, with sensible defaults for development.

TODO:
- Add LLM provider configuration
- Add browser pool configuration
- Add observability configuration
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Agentic Browser Backend"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # TODO: Add these configurations when implementing
    # LLM
    # llm_provider: str = "openai"
    # llm_model: str = "gpt-4"
    # llm_api_key: str = ""

    # Browser
    # browser_pool_size: int = 5
    # browser_timeout_ms: int = 30000
    # headless: bool = True

    # Observability
    # log_level: str = "INFO"
    # tracing_enabled: bool = False
    # tracing_endpoint: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings: The application settings singleton.
    """
    return Settings()
