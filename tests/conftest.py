from __future__ import annotations

import pytest

from parsers.source.models.ExtractedSymbol import ExtractedSymbol
from llm.models import LLMEmbeddingRequest, LLMEmbeddingResponse

TEST_DIM = 8


class FakeEmbedder:
    model = "fake-embedding-model"

    def generate_embedding(self, request: LLMEmbeddingRequest) -> LLMEmbeddingResponse:
        seed = hash(request.input) % (2 ** 31)
        vector = [
            float(((seed >> (i * 4)) & 0xFF) - 128) / 128.0
            for i in range(TEST_DIM)
        ]
        return LLMEmbeddingResponse(
            embedding=vector,
            model=self.model,
            dimensions=TEST_DIM,
        )


@pytest.fixture
def fake_embedder() -> FakeEmbedder:
    return FakeEmbedder()


@pytest.fixture
def store(monkeypatch):
    from config.settings import settings
    monkeypatch.setattr(settings, "QDRANT_URL", ":memory:")
    monkeypatch.setattr(settings, "EMBEDDING_DIMENSIONS", TEST_DIM)

    from retrieval.qdrant_client import QdrantStore
    return QdrantStore()


def make_record(
    qualified_name: str,
    vector: list[float],
    symbol_type: str = "function",
    text: str | None = None,
) -> dict:
    return {
        "text": text or f"def {qualified_name}(): pass",
        "metadata": {
            "qualified_name": qualified_name,
            "symbol_type": symbol_type,
            "class_name": None,
            "file_path": f"src/{qualified_name}.py",
        },
        "embedding": vector,
        "model": "test-model",
        "dimensions": len(vector),
    }


def make_symbol(
    name: str,
    source_code: str = "def f(): pass",
    symbol_type: str = "function",
    class_name: str | None = None,
) -> ExtractedSymbol:
    qualified = f"{class_name}.{name}" if class_name else name
    return ExtractedSymbol(
        symbol_type=symbol_type,
        name=name,
        qualified_name=qualified,
        class_name=class_name,
        file_path=f"src/{name}.py",
        source_code=source_code,
        imports=[],
        dependencies=[],
        exceptions=[],
        decorators=[],
        docstring=None,
        branches=0,
        edge_cases=[],
    )