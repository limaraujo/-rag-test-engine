from pydantic import BaseModel


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    temperature: float = 0.2
    agent: str | None = None
    label: str | None = None


class LLMResponse(BaseModel):
    content: str
    model: str
    usage: TokenUsage | None = None


class LLMEmbeddingRequest(BaseModel):
    input: str
    model: str
    label: str | None = None


class LLMEmbeddingResponse(BaseModel):
    embedding: list[float]
    model: str
    dimensions: int
    usage: TokenUsage | None = None