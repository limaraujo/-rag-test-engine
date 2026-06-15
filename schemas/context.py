from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from parsers.source.import_resolver import module_name_from_path
from parsers.source.models.ExtractedSymbol import ExtractedSymbol
from prompts.rag import build_rag_prompt_sections, rag_items_from_lists
from schemas.retrieval_context import RetrievalContext

from config.settings import settings


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
            "Lacunas de cobertura detectadas por pytest-cov: "
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

    def to_prompt_block(self, *, compact: bool = False) -> str:
        """
        Formata o contexto como bloco de texto estruturado para o prompt do LLM.

        Produz seções bem demarcadas — identificação, código, análise
        estática e contexto RAG — que o modelo consegue ler e usar
        para gerar testes mais precisos e contextualizados.

        Seções omitidas quando vazias para não poluir o prompt.
        Com ``compact=True`` (reparo), omite contexto RAG e metadados extras.

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

        if self.imports and not compact:
            parts.append(f"\n## Imports disponíveis no arquivo\n{bullet(self.imports)}")

        if self.dependencies and not compact:
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

        if not compact:
            rc = self.retrieval_context
            rag_items = rag_items_from_lists(
                dependency_functions=rc.dependency_functions if rc else None,
                callee_functions=rc.callee_functions if rc else None,
                caller_functions=rc.caller_functions if rc else None,
                related_functions=self.related_functions or None,
                similar_tests=self.similar_tests or None,
            )
            rag_sections, _ = build_rag_prompt_sections(
                rag_items,
                max_total_chars=settings.PROMPT_MAX_RAG_TOTAL_CHARS,
                max_snippet_chars=settings.PROMPT_MAX_RAG_SNIPPET_CHARS,
            )
            parts.extend(rag_sections)

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
            branch_pct = self.coverage_summary.get("branch_coverage_percent")
            threshold = self.coverage_summary.get("threshold_percent", 80)
            branch_note = (
                f", branches: {branch_pct}%"
                if branch_pct is not None
                else ""
            )
            parts.append(
                f"\n## Cobertura atual\n"
                f"  linhas: {pct}%{branch_note} (mínimo exigido: {threshold}%)"
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