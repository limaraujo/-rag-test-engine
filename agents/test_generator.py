from __future__ import annotations
 
import re
 
from llm.gemini import GeminiLLM
from llm.models import LLMRequest
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest
 
 
# ── Prompt do sistema ──────────────────────────────────────────────────────────
 
_SYSTEM_PROMPT = """
Você é um engenheiro de testes Python especialista em pytest.
 
Sua tarefa: dada uma descrição estruturada de uma função Python, escreva um arquivo de
teste pytest completo e executável que a cubra de forma abrangente.
 
FORMATO DE SAÍDA:
- APENAS código fonte Python puro.
- NÃO envolva a saída em blocos de código markdown (sem ``` ou ```python).
- Comece diretamente com as instruções de import.
- Nenhum texto ou prosa antes ou depois do código.
 
REGRAS DE IMPORTAÇÃO:
- Deduza o módulo a ser importado a partir do campo "arquivo:" no contexto.
  Exemplo: arquivo = "src/calc.py"  →  from calc import divide
  Exemplo: arquivo = "services/user_service.py"  →  from user_service import create_user
- Importe apenas o que o teste realmente usa.
 
REQUISITOS DO TESTE:
1. Uma função de teste por cenário, nomeada test_<função>_<cenário>.
2. Adicione uma docstring de uma linha a cada teste descrevendo o que ele valida.
3. Cubra TODOS os itens a seguir quando presentes no contexto:
   - Caminho feliz (happy path: entradas normais e válidas → saída esperada)
   - Cada caso de borda listado em "Casos de borda"
   - Cada exceção listada em "Exceções relevantes" → use pytest.raises()
   - Pelo menos um cenário por ramificação (use "Complexidade" como guia)
4. Para métodos (quando "classe:" estiver presente), instancie a classe primeiro.
5. Use valores concretos e significativos — não apenas 0, 1, None em todo lugar.
6. Mantenha cada teste independente (sem estado mutável compartilhado entre os testes).
7. Use unittest.mock.patch apenas quando uma dependência for um serviço externo
   (rede, banco de dados, sistema de arquivos) — NÃO faça mock da própria função sob teste.
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
 
    def __init__(self, llm: GeminiLLM | None = None) -> None:
        self._llm = llm or GeminiLLM()
 
    def generate(self, context: FunctionContext) -> GeneratedTest:
        """
        Gera um arquivo de teste pytest para o FunctionContext fornecido.
 
        Args:
            context: Contexto totalmente preenchido (com ou sem campos RAG).
 
        Retorna:
            Um GeneratedTest com código (code), imports e coverage_hints preenchidos.
        """
        request = LLMRequest(
            system_prompt=_SYSTEM_PROMPT,
            user_prompt=context.to_prompt_block(),
            temperature=0.1,
        )
        response = self._llm.generate(request)
        return _parse_response(response.content, context.qualified_name)
 
 
# ── Auxiliares de parsing (também usados pelo RepairAgent) ─────────────────────
 
def _parse_response(raw: str, qualified_name: str) -> GeneratedTest:
    code = _strip_markdown(raw)
    return GeneratedTest(
        target_function=qualified_name,
        imports=_extract_imports(code),
        code=code,
        coverage_hints=_extract_coverage_hints(code),
    )
 
 
def _strip_markdown(text: str) -> str:
    """
    Remove os blocos de código markdown quando o LLM envolve sua saída neles de qualquer forma.
 
    Lida tanto com ```python\\n...\\n``` quanto com ```\\n...\\n```.
    """
    text = text.strip()
    if not text.startswith("```"):
        return text
 
    lines = text.splitlines()
    # Remove a marcação de abertura (```python ou ```)
    lines = lines[1:]
    # Remove a marcação de fechamento se estiver presente
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
 
    return "\n".join(lines).strip()
 
 
def _extract_imports(code: str) -> list[str]:
    """Retorna todas as linhas de import de nível superior do código gerado."""
    return [
        line.strip()
        for line in code.splitlines()
        if re.match(r"^(import |from )\S", line.strip())
    ]
 
 
def _extract_coverage_hints(code: str) -> list[str]:
    """
    Constrói uma lista de dicas de cobertura (coverage-hint) a partir dos nomes das 
    funções de teste + suas docstrings.
 
    Formato: "test_divide_by_zero: Raises ValueError when divisor is 0"
    Recorre apenas ao nome da função quando nenhuma docstring for encontrada.
    """
    hints: list[str] = []
    lines = code.splitlines()
 
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("def test_"):
            continue
 
        name = stripped.split("(")[0].removeprefix("def ")
 
        # Procura mais adiante por uma docstring real (uma linha envolvida em aspas triplas)
        doc = ""
        for j in range(i + 1, min(i + 5, len(lines))):
            stripped = lines[j].strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                # Remove os marcadores de aspas e captura o conteúdo
                doc = stripped.strip('"""').strip("'''").strip()
                break
            # Para de verificar na primeira linha que não estiver em branco e não for uma docstring
            if stripped:
                break
 
        hints.append(f"{name}: {doc}" if doc else name)
 
    return hints