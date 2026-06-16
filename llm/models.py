from pydantic import BaseModel, Field


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    reasoning_tokens: int | None = None
    cached_prompt_tokens: int | None = None
    estimated_cost: float | None = None


class LLMRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    temperature: float = 0.2
    agent: str | None = None
    label: str | None = None
    operation: str | None = None
    symbol: str | None = None


class LLMResponse(BaseModel):
    content: str
    model: str
    usage: TokenUsage | None = None


class LLMEmbeddingRequest(BaseModel):
    input: str
    model: str
    label: str | None = None
    operation: str = "embedding"
    symbol: str | None = None


class LLMEmbeddingResponse(BaseModel):
    embedding: list[float]
    model: str
    dimensions: int
    usage: TokenUsage | None = None
