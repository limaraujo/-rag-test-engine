from __future__ import annotations

import hashlib
import struct

from config.settings import settings
from llm.base import BaseEmbedding
from llm.call_logger import get_call_logger
from llm.models import LLMEmbeddingRequest, LLMEmbeddingResponse


def _deterministic_vector(text: str, dimensions: int) -> list[float]:
    """Gera vetor determinístico a partir do texto (sem chamada de API)."""
    vector: list[float] = []
    for i in range(dimensions):
        digest = hashlib.sha256(f"{text}:{i}".encode()).digest()
        value = struct.unpack("f", digest[:4])[0]
        vector.append(value)

    norm = sum(v * v for v in vector) ** 0.5
    if norm:
        vector = [v / norm for v in vector]
    return vector


class LocalEmbedding(BaseEmbedding):
    """Embeddings locais para desenvolvimento sem API OpenAI."""

    def __init__(self) -> None:
        self.model = "local-deterministic"

    def generate_embedding(
        self,
        request: LLMEmbeddingRequest,
    ) -> LLMEmbeddingResponse:
        dims = settings.EMBEDDING_DIMENSIONS
        vector = _deterministic_vector(request.input, dims)
        response = LLMEmbeddingResponse(
            embedding=vector,
            model=self.model,
            dimensions=dims,
        )
        get_call_logger().log_embedding(request, response, model=self.model)
        return response
