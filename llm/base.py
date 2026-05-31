from abc import ABC, abstractmethod

from llm.models import (
    LLMEmbeddingRequest,
    LLMEmbeddingResponse,
    LLMRequest,
    LLMResponse
)


class BaseLLM(ABC):

    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        pass


class BaseEmbedding(ABC):

    @abstractmethod
    def generate_embedding(
        self,
        request: LLMEmbeddingRequest
    ) -> LLMEmbeddingResponse:
        pass