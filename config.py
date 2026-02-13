"""Configuration utilities for the regression test case generator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    llm_provider: str
    openai_api_key: str
    openai_model: str
    ollama_host: str
    requirement_file: Path
    output_file: Path


def _load_env_file(env_file: str = ".env") -> None:
    """Load environment variables on demand from the provided env file."""

    load_dotenv(dotenv_path=env_file, override=False)


def load_settings(env_file: str = ".env") -> Settings:
    """Load and validate runtime settings."""

    _load_env_file(env_file=env_file)

    llm_provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434").strip()
    requirement_file = Path(os.getenv("REQUIREMENT_FILE", "requirement.txt")).expanduser()
    output_file = Path(os.getenv("OUTPUT_FILE", "regression_test_cases.md")).expanduser()

    if llm_provider != "openai":
        raise ValueError(
            f"Unsupported LLM_PROVIDER '{llm_provider}'. Only 'openai' is supported right now."
        )

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is required. Set it in your .env file.")

    return Settings(
        llm_provider=llm_provider,
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        ollama_host=ollama_host,
        requirement_file=requirement_file,
        output_file=output_file,
    )
