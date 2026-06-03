from __future__ import annotations

from pydantic import BaseModel, Field

from ingest.models.ExtractedSymbol import ExtractedSymbol


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
    related_functions: list[str] = Field(
        default_factory=list,
        description=(
            "Código-fonte de funções similares recuperadas do banco vetorial. "
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

    @classmethod
    def from_symbol(cls, symbol: ExtractedSymbol) -> "FunctionContext":
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
        return cls(
            function_name=symbol.name,
            qualified_name=symbol.qualified_name,
            symbol_type=symbol.symbol_type,
            class_name=symbol.class_name,
            file_path=symbol.file_path,
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

        if self.related_functions:
            parts.append(
                f"\n## Funções relacionadas (contexto RAG)\n{bullet(self.related_functions)}"
            )

        if self.similar_tests:
            parts.append(
                f"\n## Testes similares existentes\n{bullet(self.similar_tests)}"
            )

        return "\n".join(parts)