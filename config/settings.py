from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):

    GEMINI_API_KEY: str = Field(...)
    
    GEMINI_MODEL: str = Field(
        default="gemini-2.5-flash"
    )
    
    GEMINI_EMBEDDING_MODEL: str = Field(
        default="gemini-embedding-001",
    )

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
    )

settings = Settings()  # type: ignore
