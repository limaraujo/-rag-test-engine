from __future__ import annotations

import ast
import logging
import re

from agents.import_utils import import_target, normalize_test_imports
from config.settings import ROOT, settings
from llm.base import BaseLLM
from llm.factory import get_llm
from llm.models import LLMRequest
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest

logger = logging.getLogger(__name__)

PROMPT_VERSION = "1"
GENERATOR_VERSION = "1"


class EmptyGenerationError(ValueError):
    """Resposta do LLM sem código de teste."""


class TruncatedGenerationError(ValueError):
    """Resposta do LLM aparentemente truncada antes de completar o código."""


def _build_system_prompt() -> str:
    max_fn = settings.GENERATION_MAX_TEST_FUNCTIONS
    max_lines = settings.GENERATION_MAX_LINES
    return f"""
Você gera testes pytest para um único símbolo Python.

SAÍDA:
- Retorne somente código Python executável.
- Sem markdown, cercas de código (```) ou explicações.
- Comece com imports; nada antes ou depois do código.
- Sem docstrings ou comentários.
- Seja conciso: o menor conjunto que ainda cubra o essencial.

IMPORTS:
- Use o campo "módulo:" do contexto como caminho de importação.
- Importe apenas o que o teste usa; não invente módulos ou símbolos.

COBERTURA (priorize nesta ordem se o limite apertar):
1. Caminho principal (happy path).
2. Exceções explicitamente listadas em "Exceções relevantes" → pytest.raises().
3. Branches relevantes (use "Complexidade" como guia).
4. Casos de borda claramente inferíveis do contexto.
- Prefira pytest.mark.parametrize para cenários equivalentes.
- Para métodos (quando "classe:" estiver presente), instancie a classe.
- Use unittest.mock.patch só para I/O externo ou dependências realmente externas.
- Não invente APIs, atributos, exceções ou fixtures ausentes no contexto.
- Se o limite não couber tudo, mantenha testes válidos e essenciais.

LIMITES (obrigatório):
- No máximo {max_fn} funções test_*.
- No máximo {max_lines} linhas no arquivo.
""".strip()


# ── Agente público ─────────────────────────────────────────────────────────────

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
            system_prompt=_build_system_prompt(),
            user_prompt=context.to_prompt_block(),
            temperature=0.1,
            agent="test_generator",
            label=f"{context.qualified_name}::{operation}",
        )
        response = self._llm.generate(request)
        return _parse_response(response.content, context)


# ── Auxiliares de parsing (também usados pelo RepairAgent) ─────────────────────

def _parse_response(raw: str, context: FunctionContext) -> GeneratedTest:
    code = _normalize_code_response(raw)
    _validate_syntax(code)
    _warn_generation_limits(code)
    module, name = import_target(context, ROOT)
    code = normalize_test_imports(code, module=module, name=name)
    return GeneratedTest(
        target_function=context.qualified_name,
        imports=_extract_imports(code),
        code=code,
        coverage_hints=_extract_coverage_hints(code),
    )


def _normalize_code_response(raw: str) -> str:
    text = raw.strip()
    if not text:
        raise EmptyGenerationError("LLM returned empty test code")

    if _has_markdown_fence(text):
        text = _strip_markdown(text)
        if not text:
            raise EmptyGenerationError("LLM returned empty test code after removing markdown fences")

    _raise_if_truncated(text, raw)
    return text


def _has_markdown_fence(text: str) -> bool:
    return text.startswith("```") or "```python" in text or re.search(r"^```\w*\s*$", text, re.MULTILINE)


def _strip_markdown(text: str) -> str:
    """
    Remove cercas markdown quando o LLM envolve a saída nelas.

    Lida com ```python\\n...\\n``` e ```\\n...\\n```.
    """
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()

    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return text


def _raise_if_truncated(code: str, raw: str) -> None:
    if raw.count("```") % 2 == 1:
        raise TruncatedGenerationError("LLM response has unclosed markdown fence")

    stripped = code.rstrip()
    if not stripped:
        raise EmptyGenerationError("LLM returned empty test code")

    last_line = stripped.splitlines()[-1].strip()
    if last_line.endswith(("\\", "(", "[", "{", ",", ":")):
        raise TruncatedGenerationError(f"LLM response ends with incomplete line: {last_line!r}")

    if re.search(r"\bdef test_\w*$", last_line):
        raise TruncatedGenerationError("LLM response ends with incomplete test function definition")


def _validate_syntax(code: str) -> None:
    ast.parse(code)


def _count_test_functions(code: str) -> int:
    return sum(
        1 for line in code.splitlines()
        if line.strip().startswith("def test_")
    )


def _warn_generation_limits(code: str) -> None:
    num_tests = _count_test_functions(code)
    num_lines = len(code.splitlines())
    max_fn = settings.GENERATION_MAX_TEST_FUNCTIONS
    max_lines = settings.GENERATION_MAX_LINES

    if num_tests > max_fn:
        logger.warning(
            "generated test has %d test functions (limit %d)",
            num_tests,
            max_fn,
        )
    if num_lines > max_lines:
        logger.warning(
            "generated test has %d lines (limit %d)",
            num_lines,
            max_lines,
        )


def _extract_imports(code: str) -> list[str]:
    """Retorna todas as linhas de import de nível superior do código gerado."""
    return [
        line.strip()
        for line in code.splitlines()
        if re.match(r"^(import |from )\S", line.strip())
    ]


def _extract_coverage_hints(code: str) -> list[str]:
    """
    Constrói dicas de cobertura a partir dos nomes das funções de teste.

    Inclui docstring de uma linha quando presente; caso contrário usa só o nome.
    """
    hints: list[str] = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("def test_"):
            continue

        name = stripped.split("(")[0].removeprefix("def ")

        parametrize_hint = ""
        for j in range(max(0, i - 3), i):
            prev = lines[j].strip()
            if prev.startswith("@pytest.mark.parametrize"):
                parametrize_hint = " (parametrize)"
                break

        doc = ""
        for j in range(i + 1, min(i + 5, len(lines))):
            inner = lines[j].strip()
            if inner.startswith('"""') or inner.startswith("'''"):
                doc = inner.strip('"""').strip("'''").strip()
                break
            if inner:
                break

        label = f"{name}{parametrize_hint}"
        hints.append(f"{label}: {doc}" if doc else label)

    return hints
