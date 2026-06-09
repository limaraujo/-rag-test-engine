from google import genai

from config.settings import settings
from llm.base import BaseEmbedding
from llm.models import LLMEmbeddingRequest, LLMEmbeddingResponse


class GeminiEmbedding(BaseEmbedding):
    """Gemini embedding client wrapper."""

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_EMBEDDING_MODEL

    def generate_embedding(
        self,
        request: LLMEmbeddingRequest
    ) -> LLMEmbeddingResponse:
        model = request.model or self.model
        response = self.client.models.embed_content(
            model=model,
            contents=request.input
        )

        if not response.embeddings:
            raise RuntimeError(
                "No embedding response from Gemini API"
            )

        vector = response.embeddings[0].values

        return LLMEmbeddingResponse(
            embedding=vector,
            model=model,
            dimensions=len(vector)
        )