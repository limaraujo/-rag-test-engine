from openai import OpenAI

from config.settings import settings
from llm.base import BaseEmbedding
from llm.call_logger import get_call_logger
from llm.models import LLMEmbeddingRequest, LLMEmbeddingResponse
from llm.token_usage import token_usage_from_openai
from llm.usage_tracker import get_tracker


class OpenAIEmbedding(BaseEmbedding):
    """OpenAI embedding client wrapper."""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_EMBEDDING_MODEL

    def generate_embedding(
        self,
        request: LLMEmbeddingRequest,
    ) -> LLMEmbeddingResponse:
        model = request.model or self.model
        response = self.client.embeddings.create(
            model=model,
            input=request.input,
            dimensions=settings.EMBEDDING_DIMENSIONS,
        )

        vector = response.data[0].embedding

        usage = token_usage_from_openai(response.usage, model=model)
        if usage:
            get_tracker().record_embedding(
                usage,
                model=model,
                label=request.label,
                symbol=request.symbol,
            )

        embedding_response = LLMEmbeddingResponse(
            embedding=vector,
            model=model,
            dimensions=len(vector),
            usage=usage,
        )
        get_call_logger().log_embedding(request, embedding_response, model=model)
        return embedding_response
