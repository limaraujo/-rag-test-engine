from __future__ import annotations

from config.settings import settings
from llm.base import BaseLLM
from llm.factory import get_llm
from llm.models import LLMRequest
from parsers.llm.response import parse_response
from prompts.loader import load_repair_system_prompt
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest


class RepairAgent:
    """
    Corrige um :class:`~schemas.outputs.GeneratedTest` que falhou ao ser executado com o pytest.

    Alimenta o LLM com o contexto original, o código que falhou e a saída de erro do pytest, 
    solicitando que ele produza um arquivo de teste corrigido.

    Projetado para ser usado em um loop de repetição (retry loop)::

        runner = TestRunner()
        repair = RepairAgent()

        result = runner.run(test, pythonpath=[...])
        for attempt in range(1, max_attempts + 1):
            if result.passed:
                break
            test   = repair.repair(ctx, test, result, attempt=attempt)
            result = runner.run(test, pythonpath=[...])
    """

    def __init__(self, llm: BaseLLM | None = None) -> None:
        self._llm = llm or get_llm()

    def repair(
        self,
        ctx: FunctionContext,
        failing_test: GeneratedTest,
        run_result: "RunResult",  # noqa: F821  (evita importação circular)
        *,
        attempt: int = 1,
    ) -> GeneratedTest:
        """
        Tenta corrigir o *failing_test* usando o LLM.

        Args:
            ctx:          Contexto da função sob teste.
            failing_test: O :class:`GeneratedTest` que gerou falhas.
            run_result:   O :class:`~execution.runner.RunResult` da
                          última execução do pytest — seu ``failure_summary`` é fornecido
                          ao modelo.
            attempt:      Número da tentativa atual (mostrado ao modelo para que ele saiba
                          quantos reparos já foram tentados).

        Retorna:
            Um novo :class:`GeneratedTest` com o código (esperançosamente) corrigido.
        """
        user_prompt = _build_repair_prompt(ctx, failing_test, run_result, attempt)

        request = LLMRequest(
            system_prompt=load_repair_system_prompt(),
            user_prompt=user_prompt,
            temperature=0.1,
            agent="repair",
            label=f"{ctx.qualified_name}::repair_{attempt}",
            operation=f"repair_{attempt}",
            symbol=ctx.qualified_name,
        )

        response = self._llm.generate(request)
        return parse_response(response.content, ctx)


# ── Auxiliares ─────────────────────────────────────────────────────────────────

def _build_repair_prompt(
    ctx: FunctionContext,
    test: GeneratedTest,
    run_result: "RunResult",
    attempt: int,
) -> str:
    """Monta o prompt de reparo completo enviado ao LLM."""
    error_block = (run_result.failure_summary or "").strip()
    if not error_block:
        error_block = run_result.output.strip()
    max_chars = settings.REPAIR_ERROR_MAX_CHARS
    if len(error_block) > max_chars:
        error_block = error_block[:max_chars] + "\n… (truncado)"

    return "\n".join([
        f"# Tentativa de reparo {attempt}",
        "",
        "## Função sob teste",
        ctx.to_prompt_block(compact=True),
        "",
        "## Arquivo de teste falho",
        "```python",
        test.full_code,
        "```",
        "",
        "## Saída de erro do pytest",
        "```",
        error_block,
        "```",
        "",
        "Gere apenas o arquivo de teste Python corrigido.",
    ])
