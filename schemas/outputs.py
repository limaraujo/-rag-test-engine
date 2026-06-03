from __future__ import annotations

from pydantic import BaseModel, Field


class GeneratedTest(BaseModel):
    """
    Saída estruturada do gerador de testes.

    Representa um arquivo de teste completo,
    pronto para ser salvo em disco e executado com pytest.

    O campo `code` sempre contém o arquivo inteiro (imports incluídos).
    O campo `imports` é a lista extraída linha a linha — útil para
    inspecionar se o modelo inventou dependências que não existem.
    """

    # Identificação
    target_function: str = Field(
        ...,
        description="Nome qualificado da função ou método sendo testado."
    )

    # Conteúdo do arquivo de teste
    imports: list[str] = Field(
        default_factory=list,
        description=(
            "Linhas de import extraídas do teste gerado. "
            "Use para validar que o modelo não inventou dependências."
        )
    )
    code: str = Field(
        ...,
        description=(
            "Código completo do arquivo de teste, incluindo imports. "
            "Pronto para ser salvo como .py e executado com pytest."
        )
    )

    # Metadados de qualidade
    coverage_hints: list[str] = Field(
        default_factory=list,
        description=(
            "Descrição do que cada teste cobre: branches, edge cases, cenários. "
            "Útil para logging, debug e relatórios de qualidade."
        )
    )

    @property
    def full_code(self) -> str:
        """
        Retorna o código completo do arquivo de teste.

        Se `code` já inclui os imports (caso normal quando o modelo
        retorna o arquivo inteiro), retorna `code` diretamente.
        Caso contrário, monta: imports no topo + code abaixo.

        Exemplo de uso no runner:
            test_path = tmp_dir / f"test_{target}.py"
            test_path.write_text(generated.full_code, encoding="utf-8")
        """
        if not self.imports:
            return self.code

        import_block = "\n".join(self.imports)
        if import_block in self.code:
            return self.code

        return f"{import_block}\n\n{self.code}"

    def has_import(self, module: str) -> bool:
        """
        Verifica se um módulo específico foi importado pelo teste gerado.

        Útil para detectar se o modelo inventou um import inexistente:

            if not generated.has_import("myapp.services"):
                # modelo aluciou — acionar repair ou rejeitar
                raise ValueError(f"import inexistente: myapp.services")
        """
        return any(module in line for line in self.imports)

    def test_function_names(self) -> list[str]:
        """
        Extrai os nomes das funções de teste do código gerado.

        Faz parsing linha a linha — não exige AST.
        Retorna apenas funções que começam com 'test_'.

        Exemplo de uso:
            names = generated.test_function_names()
            print(f"Gerou {len(names)} testes: {names}")
            # ['test_divide_normal', 'test_divide_by_zero']
        """
        names: list[str] = []
        for line in self.code.splitlines():
            stripped = line.strip()
            if stripped.startswith("def test_"):
                name = stripped.split("(")[0].removeprefix("def ")
                names.append(name)
        return names