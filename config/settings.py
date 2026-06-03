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

    # ── Qdrant ──────────────────────────────────────────────────────────
    # Use ":memory:" para testes, ou URL para produção.
    # Ex:
    #   QDRANT_URL=:memory:
    #   QDRANT_URL=http://localhost:6333
    #   QDRANT_URL=https://xyz.cloud.qdrant.io
    QDRANT_URL: str = Field(
        default="http://localhost:6333",
    )

        QDRANT_API_KEY: str | None = Field(
        default=None,
        description="Qdrant Cloud API key. Not needed for local instances.",
    )

    #Chave de API do Qdrant Cloud. Não é necessária para instâncias locais.
    QDRANT_API_KEY: str | None = Field(
        default=None,
    )

    #Coleção que armazena embeddings de símbolos do código de produção.
    QDRANT_COLLECTION_SYMBOLS: str = Field(
        default="symbols",
    )

    #Coleção que armazena embeddings de testes existentes.
    QDRANT_COLLECTION_TESTS: str = Field(
        default="tests",
    )

    # Deve corresponder à dimensionalidade de saída do modelo de embeddings.
    # gemini-embedding-001 → 3072 (dimensões padrão de saída).
    EMBEDDING_DIMENSIONS: int = Field(
        default=3072,
    )

    # ── Configurações padrão de recuperação
    #Quantidade de trechos de funções relacionadas recuperados por consulta.
    RETRIEVER_TOP_K_FUNCTIONS: int = Field(
        default=3,
    )

    #Quantidade de trechos de testes semelhantes recuperados por consulta.
    RETRIEVER_TOP_K_TESTS: int = Field(
        default=3,
    )

    #Pontuação mínima de similaridade cosseno aceita (0 – 1).
    RETRIEVER_SCORE_THRESHOLD: float = Field(
        default=0.55,
    )

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
    )

settings = Settings()  # type: ignore
