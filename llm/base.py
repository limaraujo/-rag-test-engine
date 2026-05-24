from abc import ABC, abstractmethod

from llm.models import LLMRequest, LLMResponse


class BaseLLM(ABC):

    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        pass