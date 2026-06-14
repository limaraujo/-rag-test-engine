from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):

    OPENAI_API_KEY: str = Field(...)

    # "openai" = API real; "offline" = embeddings e LLM locais (sem créditos).
    AI_MODE: str = Field(
        default="openai",
    )

    OPENAI_MODEL: str = Field(
        default="gpt-5-nano",
    )

    OPENAI_EMBEDDING_MODEL: str = Field(
        default="text-embedding-3-small",
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

    #Coleção que armazena embeddings de símbolos do código de produção.
    QDRANT_COLLECTION_SYMBOLS: str = Field(
        default="symbols",
    )

    #Coleção que armazena embeddings de testes existentes.
    QDRANT_COLLECTION_TESTS: str = Field(
        default="tests",
    )

    # Deve corresponder à dimensionalidade de saída do modelo de embeddings.
    # text-embedding-3-small → 1536 (dimensões padrão de saída).
    EMBEDDING_DIMENSIONS: int = Field(
        default=1536,
    )

    # Se false, só gera embedding de símbolos novos ou alterados (reutiliza Qdrant).
    REINDEX_SYMBOLS: bool = Field(
        default=False,
    )

    GENERATION_CACHE_ENABLED: bool = Field(
        default=True,
        description="Reutiliza testes aprovados do cache persistente antes de chamar o LLM.",
    )

    GENERATION_CACHE_DIR: str = Field(
        default="",
        description=(
            "Diretório do cache de geração (fora do workspace temporal). "
            "Vazio = .cache/generation na raiz do projeto."
        ),
    )

    GENERATION_CACHE_SCHEMA_VERSION: int = Field(
        default=1,
        description="Versão do schema JSON das entradas do cache de geração.",
    )

    RUNS_DIR: str = Field(
        default="runs",
        description="Raiz das pastas de execução (runs/<fonte>/<timestamp>/).",
    )

    LOG_DIR: str = Field(
        default="logs",
        description="Fallback de logs quando setup_logging não recebe caminho.",
    )

    LOG_LEVEL: str = Field(
        default="INFO",
        description="Nível de log: DEBUG, INFO, WARNING, ERROR.",
    )

    LOG_API_CALLS: bool = Field(
        default=True,
        description=(
            "Grava chamadas LLM/embedding em logs/api_calls/ do workspace."
        ),
    )

    LOG_API_CALL_BODIES: bool = Field(
        default=False,
        description="Quando true, persiste prompt e resposta integral nos logs de API.",
    )

    LOG_API_CALL_METADATA: bool = Field(
        default=True,
        description="Inclui metadados (tamanhos, operação, símbolo) nos logs de API.",
    )

    LLM_PRICING_JSON: str = Field(
        default="",
        description=(
            "JSON opcional de preços por modelo (USD / 1M tokens). "
            'Ex.: {"gpt-5-nano":{"input":0.05,"output":0.40}}'
        ),
    )

    # ── Configurações padrão de recuperação
    #Quantidade final de resultados após reranking híbrido.
    RETRIEVER_TOP_K: int = Field(
        default=3,
    )

    #Quantidade de trechos de funções relacionadas recuperados por consulta.
    RETRIEVER_TOP_K_FUNCTIONS: int = Field(
        default=3,
    )

    #Quantidade de trechos de testes semelhantes recuperados por consulta.
    RETRIEVER_TOP_K_TESTS: int = Field(
        default=2,
    )

    #Candidatos vetoriais buscados antes do reranking híbrido.
    RETRIEVER_RERANK_POOL_SIZE: int = Field(
        default=10,
    )

    #Pesos do score híbrido (devem somar 1.0).
    RETRIEVER_VECTOR_WEIGHT: float = Field(default=0.5)
    RETRIEVER_DEPENDENCY_WEIGHT: float = Field(default=0.3)
    RETRIEVER_CALL_GRAPH_WEIGHT: float = Field(default=0.2)

    #Pontuação mínima de similaridade cosseno aceita (0 – 1).
    #0.55 filtra ruído semântico fraco; aumente para prompts mais enxutos.
    RETRIEVER_SCORE_THRESHOLD: float = Field(
        default=0.55,
        description=(
            "Similaridade cosseno mínima (0–1) para candidatos vetoriais. "
            "Valores mais altos reduzem recall; mais baixos aumentam ruído."
        ),
    )

    #Percentual mínimo de cobertura de linhas para aceitar um teste gerado.
    COVERAGE_THRESHOLD: float = Field(
        default=80.0,
    )

    #Tentativas de regeneração quando cobertura fica abaixo do threshold (0 = desligado).
    MAX_COVERAGE_ROUNDS: int = Field(
        default=0,
        description="Rodadas extras de geração por cobertura. 0 desliga o loop.",
    )

    #Interrompe regeneração quando a cobertura não aumenta entre rodadas.
    COVERAGE_STOP_ON_NO_IMPROVEMENT: bool = Field(
        default=True,
    )

    #Tentativas de reparo via LLM quando pytest falha.
    MAX_REPAIRS: int = Field(
        default=1,
    )

    #Limite global de chamadas LLM (geração + reparo + cobertura) por símbolo.
    MAX_LLM_CALLS_PER_SYMBOL: int = Field(
        default=2,
        description="Perfil econômico: 1 geração + 1 reparo. Cache hit não consome.",
    )

    #Limite de tokens de saída do LLM (None = sem limite na API).
    LLM_MAX_OUTPUT_TOKENS: int | None = Field(
        default=1536,
    )

    #Limites solicitados ao LLM na geração de testes (validados após parsing).
    GENERATION_MAX_TEST_FUNCTIONS: int = Field(
        default=4,
        description="Máximo de funções test_* por arquivo gerado.",
    )

    GENERATION_MAX_LINES: int = Field(
        default=80,
        description="Máximo de linhas no arquivo de teste gerado.",
    )

    #Funções de módulo ignoradas na geração (separadas por vírgula).
    INGEST_SKIP_FUNCTION_NAMES: str = Field(
        default="main",
    )

    #Diretórios extras ignorados na ingestão (separados por vírgula; mesclados aos padrões).
    INGEST_SKIP_DIRS: str = Field(
        default="",
        description=(
            "Nomes de diretório ignorados na varredura. Mesclado com padrões "
            "como tests/, runs/, __pycache__/, etc."
        ),
    )

    #Globs extras de arquivo ignorados na ingestão (separados por vírgula; mesclados aos padrões).
    INGEST_SKIP_FILE_GLOBS: str = Field(
        default="",
        description=(
            "Globs de nome de arquivo ignorados na varredura e na geração. "
            "Mesclado com padrões como test_*.py, conftest.py, etc."
        ),
    )

    #Orçamento global (corpo dos snippets RAG) no prompt do LLM.
    PROMPT_MAX_RAG_TOTAL_CHARS: int = Field(
        default=2500,
        description=(
            "Limite de caracteres para o corpo dos trechos RAG. "
            "Cabeçalhos de seção ficam fora deste orçamento."
        ),
    )

    #Tamanho máximo de cada trecho RAG no prompt do LLM.
    PROMPT_MAX_RAG_SNIPPET_CHARS: int = Field(
        default=300,
    )

    #Tamanho máximo do bloco de erro do pytest no prompt de reparo.
    REPAIR_ERROR_MAX_CHARS: int = Field(
        default=900,
    )

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
    )

settings = Settings()  # type: ignore
