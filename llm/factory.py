from __future__ import annotations

from config.settings import settings
from llm.base import BaseEmbedding, BaseLLM
from llm.local_embedding import LocalEmbedding
from llm.mock_llm import MockLLM
from llm.openai_embedding import OpenAIEmbedding
from llm.openai_llm import OpenAILLM


def get_embedder() -> BaseEmbedding:
    if settings.AI_MODE == "offline":
        return LocalEmbedding()
    return OpenAIEmbedding()


def get_llm() -> BaseLLM:
    if settings.AI_MODE == "offline":
        return MockLLM()
    return OpenAILLM()
