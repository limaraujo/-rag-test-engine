from __future__ import annotations

import logging

from config.settings import settings
from llm.base import BaseLLM
from llm.factory import get_llm
from llm.models import LLMRequest
from parsers.llm.response import parse_response
from prompts.loader import build_generator_system_prompt
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest

logger = logging.getLogger(__name__)

PROMPT_VERSION = "2"
GENERATOR_VERSION = "1"


class TestGeneratorAgent:
    """
    Gera um arquivo de teste pytest completo a partir de um FunctionContext.

    Usa o LLM para escrever os testes, depois analisa a saída bruta (raw) em um
    GeneratedTest estruturado, pronto para ser salvo e executado.

    Exemplo::

        agent = TestGeneratorAgent()
        ctx   = FunctionContext.from_symbol(symbol)
        test  = agent.generate(ctx)
        print(test.full_code)
    """

    def __init__(self, llm: BaseLLM | None = None) -> None:
        self._llm = llm or get_llm()

    @property
    def model_name(self) -> str:
        return getattr(self._llm, "model", settings.OPENAI_MODEL)

    def generate(
        self,
        context: FunctionContext,
        *,
        operation: str = "generate",
    ) -> GeneratedTest:
        """
        Gera um arquivo de teste pytest para o FunctionContext fornecido.

        Args:
            context: Contexto totalmente preenchido (com ou sem campos RAG).
            operation: Identificador da operação (ex.: generate, coverage_1).

        Retorna:
            Um GeneratedTest com código (code), imports e coverage_hints preenchidos.
        """
        request = LLMRequest(
            system_prompt=build_generator_system_prompt(
                max_test_functions=settings.GENERATION_MAX_TEST_FUNCTIONS,
                max_lines=settings.GENERATION_MAX_LINES,
            ),
            user_prompt=context.to_prompt_block(),
            temperature=0.1,
            agent="test_generator",
            label=f"{context.qualified_name}::{operation}",
            operation=operation,
            symbol=context.qualified_name,
        )
        response = self._llm.generate(request)
        return parse_response(response.content, context)
