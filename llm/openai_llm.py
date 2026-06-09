from openai import OpenAI

from config.settings import settings
from llm.base import BaseLLM
from llm.models import LLMRequest, LLMResponse, TokenUsage
from llm.usage_tracker import get_tracker

# Modelos de raciocínio (gpt-5*, o1/o3/o4) aceitam só temperature=1 (padrão).
_NO_CUSTOM_TEMPERATURE_PREFIXES = ("gpt-5", "o1", "o3", "o4")


def _supports_custom_temperature(model: str) -> bool:
    lowered = model.lower()
    return not any(lowered.startswith(p) for p in _NO_CUSTOM_TEMPERATURE_PREFIXES)


class OpenAILLM(BaseLLM):

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def generate(self, request: LLMRequest) -> LLMResponse:
        kwargs: dict = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
        }
        if _supports_custom_temperature(self.model):
            kwargs["temperature"] = request.temperature

        response = self.client.chat.completions.create(**kwargs)

        choice = response.choices[0].message.content
        if not choice:
            raise RuntimeError("No response from OpenAI API")

        usage = None
        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )
            get_tracker().record_llm(usage)

        return LLMResponse(
            content=choice,
            model=self.model,
            usage=usage,
        )
