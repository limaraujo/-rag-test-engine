from __future__ import annotations

from agents.test_generator import _parse_response
from llm.gemini import GeminiLLM
from llm.models import LLMRequest
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest


_REPAIR_SYSTEM_PROMPT = """
Você é um engenheiro de testes Python especialista. Um arquivo de teste pytest gerado falhou.

Sua tarefa: corrigir o código que falhou para que TODOS os testes passem.

FORMATO DE SAÍDA:
- APENAS código-fonte Python puro.
- NÃO envolva a saída em blocos de código markdown (sem ``` ou ```python).
- Comece diretamente com as instruções de import.
- Nenhum texto ou prosa antes ou depois do código.

ESTRATÉGIA DE REPARO:
1. Leia a saída de erro com atenção para entender a causa raiz.
2. Problemas comuns e correções:
   - ImportError / ModuleNotFoundError → corrija o caminho de importação usando o 
     campo "arquivo:" no contexto (ex: "src/calc.py" → "from calc import …")
   - TypeError (argumentos incorretos) → corrija a chamada para corresponder à assinatura real
   - AssertionError → corrija o valor esperado para corresponder ao comportamento real
   - AttributeError → o nome da classe/função pode estar errado; verifique o contexto
   - NameError → adicione o import ausente ou corrija o identificador
3. Mantenha todos os testes que já estavam corretos.
4. NÃO remova casos de teste — em vez disso, corrija-os.
5. NÃO altere o que está sendo testado; apenas corrija como é chamado ou verificado (assert).
""".strip()


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

    def __init__(self, llm: GeminiLLM | None = None) -> None:
        self._llm = llm or GeminiLLM()

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
            system_prompt=_REPAIR_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.1,
        )

        response = self._llm.generate(request)
        return _parse_response(response.content, ctx.qualified_name)


# ── Auxiliares ─────────────────────────────────────────────────────────────────

def _build_repair_prompt(
    ctx: FunctionContext,
    test: GeneratedTest,
    run_result: "RunResult",
    attempt: int,
) -> str:
    """Monta o prompt de reparo completo enviado ao LLM."""
    error_block = run_result.failure_summary or run_result.output
    # Limite rígido para a saída de erro para não estourar a janela de contexto
    if len(error_block) > 3000:
        error_block = error_block[:3000] + "\n… (truncado)"

    return "\n".join([
        f"# Tentativa de reparo {attempt}",
        "",
        "## Função sob teste",
        ctx.to_prompt_block(),
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