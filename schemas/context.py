from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from ingest.import_resolver import module_name_from_path
from ingest.models.ExtractedSymbol import ExtractedSymbol
from schemas.retrieval_context import RetrievalContext


class FunctionContext(BaseModel):
    """
    Entrada do gerador de testes.

    Agrega toda a informação estática e contextual que o modelo
    precisa para gerar testes inteligentes e cobrir branches reais.

    Pode ser construído de duas formas:

    1. Sem RAG — direto do ExtractedSymbol (bootstrap rápido):
       ctx = FunctionContext.from_symbol(symbol)

    2. Com RAG — após busca no banco vetorial:
       ctx = FunctionContext.from_symbol(symbol)
       ctx = ctx.model_copy(update={
           "related_functions": [...],
           "similar_tests": [...]
       })
    """

    # Identificação
    function_name: str = Field(
        ...,
        description="Nome simples da função ou método."
    )
    qualified_name: str = Field(
        ...,
        description="Nome qualificado, ex: 'Calculadora.divide'."
    )
    symbol_type: str = Field(
        ...,
        description="'function', 'method' ou 'class'."
    )
    class_name: str | None = Field(
        default=None,
        description="Classe dona do símbolo, se for método."
    )
    file_path: str = Field(
        ...,
        description="Caminho do arquivo de origem."
    )
    module_name: str = Field(
        default="",
        description="Nome do módulo Python (ex: mockes.exemplo) relativo à raiz do projeto.",
    )

    # Código
    code: str = Field(
        ...,
        description="Código-fonte bruto do símbolo a ser testado."
    )
    docstring: str | None = Field(
        default=None,
        description="Docstring extraída do símbolo, se existir."
    )

    # Análise estática (preenchida pelo ingest)
    imports: list[str] = Field(
        default_factory=list,
        description="Imports do arquivo onde o símbolo está definido."
    )
    dependencies: list[str] = Field(
        default_factory=list,
        description="Funções, métodos e classes chamadas pelo símbolo."
    )
    exceptions: list[str] = Field(
        default_factory=list,
        description="Exceções lançadas ou capturadas pelo símbolo."
    )
    decorators: list[str] = Field(
        default_factory=list,
        description="Decoradores aplicados ao símbolo."
    )
    branches: int = Field(
        default=0,
        description="Número de desvios de fluxo (aproximação de complexidade ciclomática)."
    )
    edge_cases: list[str] = Field(
        default_factory=list,
        description="Casos de borda inferidos por heurísticas estáticas."
    )

    # Contexto RAG (preenchido pelo retriever, opcional)
    retrieval_context: RetrievalContext | None = Field(
        default=None,
        description="Contexto híbrido completo (vetor + call graph + dependency graph).",
    )
    related_functions: list[str] = Field(
        default_factory=list,
        description=(
            "Código-fonte de funções similares recuperadas por busca híbrida. "
            "Serve como contexto de implementação para o modelo."
        )
    )
    similar_tests: list[str] = Field(
        default_factory=list,
        description=(
            "Testes existentes similares, recuperados do banco vetorial. "
            "O modelo aprende padrões e convenções do projeto."
        )
    )

    # Feedback de cobertura (preenchido pelo CoverageAnalyzer entre rodadas)
    coverage_gaps: list[dict] = Field(
        default_factory=list,
        description=(
            "Lacunas de cobertura detectadas por coverage.py: "
            "file_path, function_name, uncovered_lines."
        ),
    )
    coverage_summary: dict | None = Field(
        default=None,
        description="Resumo JSON da última análise de cobertura.",
    )

    @classmethod
    def from_symbol(
        cls,
        symbol: ExtractedSymbol,
        *,
        project_root: Path | None = None,
    ) -> "FunctionContext":
        """
        Constrói um FunctionContext diretamente de um ExtractedSymbol.

        Caminho sem RAG: útil para bootstrap, testes rápidos e
        validação do pipeline antes de ter o banco vetorial pronto.
        Os campos `related_functions` e `similar_tests` ficam vazios.

        Exemplo:
            for symbol in parse_repository_symbols("src/"):
                ctx = FunctionContext.from_symbol(symbol)
                test = generator.generate(ctx)
        """
        module_name = ""
        if project_root is not None:
            module_name = module_name_from_path(
                project_root,
                Path(symbol.file_path),
            )

        return cls(
            function_name=symbol.name,
            qualified_name=symbol.qualified_name,
            symbol_type=symbol.symbol_type,
            class_name=symbol.class_name,
            file_path=symbol.file_path,
            module_name=module_name,
            code=symbol.source_code,
            docstring=symbol.docstring,
            imports=symbol.imports,
            dependencies=symbol.dependencies,
            exceptions=symbol.exceptions,
            decorators=symbol.decorators,
            branches=symbol.branches,
            edge_cases=symbol.edge_cases,
        )

    def to_prompt_block(self) -> str:
        """
        Formata o contexto como bloco de texto estruturado para o prompt do LLM.

        Produz seções bem demarcadas — identificação, código, análise
        estática e contexto RAG — que o modelo consegue ler e usar
        para gerar testes mais precisos e contextualizados.

        Seções omitidas quando vazias para não poluir o prompt.

        Exemplo de uso no test_generator:
            user_prompt = context.to_prompt_block()
            request = LLMRequest(system_prompt=SYSTEM, user_prompt=user_prompt)
        """
        def bullet(lst: list[str]) -> str:
            return (
                "\n".join(f"  - {item}" for item in lst)
                if lst
                else "  (nenhum)"
            )

        parts: list[str] = [
            "## Função alvo",
            f"nome: {self.qualified_name}",
            f"tipo: {self.symbol_type}",
            f"arquivo: {self.file_path}",
        ]

        if self.module_name:
            parts.append(f"módulo: {self.module_name}")

        if self.class_name:
            parts.append(f"classe: {self.class_name}")

        if self.docstring:
            parts.append(f"\ndocstring:\n  {self.docstring}")

        parts += [
            "\n## Código-fonte",
            "```python",
            self.code,
            "```",
        ]

        if self.imports:
            parts.append(f"\n## Imports disponíveis no arquivo\n{bullet(self.imports)}")

        if self.dependencies:
            parts.append(f"\n## Dependências chamadas\n{bullet(self.dependencies)}")

        if self.exceptions:
            parts.append(f"\n## Exceções relevantes\n{bullet(self.exceptions)}")

        if self.edge_cases:
            parts.append(f"\n## Casos de borda detectados\n{bullet(self.edge_cases)}")

        if self.branches > 0:
            parts.append(
                f"\n## Complexidade\n"
                f"  {self.branches} branch(es) — cubra ao menos um cenário por branch"
            )

        rc = self.retrieval_context
        if rc and rc.caller_functions:
            parts.append(
                f"\n## Funções chamadoras (call graph)\n{bullet(rc.caller_functions)}"
            )

        if rc and rc.callee_functions:
            parts.append(
                f"\n## Funções chamadas (call graph)\n{bullet(rc.callee_functions)}"
            )

        if rc and rc.dependency_functions:
            parts.append(
                f"\n## Dependências estruturais (dependency graph)\n"
                f"{bullet(rc.dependency_functions)}"
            )

        if self.related_functions:
            parts.append(
                f"\n## Funções relacionadas (busca híbrida)\n{bullet(self.related_functions)}"
            )

        if self.similar_tests:
            parts.append(
                f"\n## Testes similares existentes\n{bullet(self.similar_tests)}"
            )

        if self.coverage_gaps:
            gap_lines = []
            for gap in self.coverage_gaps:
                lines = gap.get("uncovered_lines", [])
                lines_str = ", ".join(str(n) for n in lines)
                gap_lines.append(
                    f"  - {gap.get('function_name', '?')}: "
                    f"linhas não cobertas [{lines_str}]"
                )
            parts.append(
                "\n## Lacunas de cobertura (PRIORIDADE — gere testes para cobrir)\n"
                + "\n".join(gap_lines)
            )

        if self.coverage_summary and not self.coverage_summary.get("meets_threshold"):
            pct = self.coverage_summary.get("line_coverage_percent", 0)
            threshold = self.coverage_summary.get("threshold_percent", 80)
            parts.append(
                f"\n## Cobertura atual\n"
                f"  {pct}% (mínimo exigido: {threshold}%)"
            )
            branches = self.coverage_summary.get("uncovered_branches", [])
            if branches:
                branch_lines = [
                    f"  - {b['function_name']}: branch {b['from_line']}→{b['to_line']}"
                    for b in branches
                ]
                parts.append(
                    "\n## Branches não cobertos\n" + "\n".join(branch_lines)
                )
            uncovered_fns = self.coverage_summary.get("uncovered_functions", [])
            if uncovered_fns:
                fn_lines = [
                    f"  - {f['function_name']}" for f in uncovered_fns
                ]
                parts.append(
                    "\n## Funções sem cobertura\n" + "\n".join(fn_lines)
                )

        return "\n".join(parts)