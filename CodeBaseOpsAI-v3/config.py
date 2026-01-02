"""
Production configuration management.

Environment-aware configuration with validation and secrets management.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

load_dotenv()


class AppConfig(BaseModel):
    """Application configuration with validation."""

    # LLM Configuration
    model_name: str = Field(
        default=os.getenv("MODEL_NAME", "gemini-2.0-flash-exp"),
        description="LLM model name"
    )
    temperature: float = Field(
        default=float(os.getenv("TEMPERATURE", "0.0")),
        ge=0.0,
        le=2.0,
        description="Model temperature"
    )
    max_retries: int = Field(
        default=int(os.getenv("MAX_RETRIES", "3")),
        ge=0,
        description="Maximum retry attempts"
    )
    timeout: float = Field(
        default=float(os.getenv("TIMEOUT", "60.0")),
        gt=0,
        description="Request timeout in seconds"
    )

    # GitHub Configuration
    github_token: Optional[str] = Field(
        default=os.getenv("GITHUB_TOKEN"),
        description="GitHub personal access token"
    )
    github_api_url: str = Field(
        default=os.getenv("GITHUB_API_URL", "https://api.github.com"),
        description="GitHub API base URL"
    )

    # Agent Configuration
    enable_checkpointing: bool = Field(
        default=os.getenv("ENABLE_CHECKPOINTING", "true").lower() == "true",
        description="Enable state checkpointing"
    )
    max_iterations: int = Field(
        default=int(os.getenv("MAX_ITERATIONS", "15")),
        ge=1,
        description="Maximum agent iterations"
    )

    # Logging Configuration
    log_level: str = Field(
        default=os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level"
    )

    # Observability
    enable_tracing: bool = Field(
        default=os.getenv("ENABLE_TRACING", "false").lower() == "true",
        description="Enable LangSmith tracing"
    )
    langsmith_api_key: Optional[str] = Field(
        default=os.getenv("LANGSMITH_API_KEY"),
        description="LangSmith API key for tracing"
    )
    langsmith_project: str = Field(
        default=os.getenv("LANGSMITH_PROJECT", "codebaseopsai"),
        description="LangSmith project name"
    )

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


# Global config instance
config = AppConfig()


def get_config() -> AppConfig:
    """Get application configuration."""
    return config
