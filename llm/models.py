from pydantic import BaseModel


class LLMRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    temperature: float = 0.2


class LLMResponse(BaseModel):
    content: str 
    model: str

class LLMEmbeddingRequest(BaseModel):
    input: str
    model: str
    
class LLMEmbeddingResponse(BaseModel):
    embedding: list[float]
    model: str
    dimensions: int