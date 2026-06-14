from __future__ import annotations

from pathlib import Path

from ingest.models.ExtractedSymbol import ExtractedSymbol
from ingest.parser import parse_file_symbols
from ingest.symbol_filter import filter_symbols


def _symbol(
    *,
    symbol_type: str = "function",
    name: str = "foo",
    qualified_name: str | None = None,
    class_name: str | None = None,
    file_path: str = "sample.py",
    source_code: str | None = None,
) -> ExtractedSymbol:
    qname = qualified_name if qualified_name is not None else name
    code = source_code or f"def {name}(): pass"
    return ExtractedSymbol(
        symbol_type=symbol_type,
        name=name,
        qualified_name=qname,
        class_name=class_name,
        file_path=file_path,
        source_code=code,
        docstring=None,
        imports=[],
        dependencies=[],
        exceptions=[],
        decorators=[],
        branches=0,
        edge_cases=[],
    )


def _class_with_three_methods() -> list[ExtractedSymbol]:
    file_path = "calc.py"
    return [
        _symbol(
            symbol_type="class",
            name="Calculadora",
            source_code=(
                "class Calculadora:\n"
                "    def alpha(self): return 1\n"
                "    def beta(self): return 2\n"
                "    def gamma(self): return 3\n"
            ),
            file_path=file_path,
        ),
        _symbol(
            symbol_type="method",
            name="alpha",
            qualified_name="Calculadora.alpha",
            class_name="Calculadora",
            file_path=file_path,
            source_code="def alpha(self): return 1",
        ),
        _symbol(
            symbol_type="method",
            name="beta",
            qualified_name="Calculadora.beta",
            class_name="Calculadora",
            file_path=file_path,
            source_code="def beta(self): return 2",
        ),
        _symbol(
            symbol_type="method",
            name="gamma",
            qualified_name="Calculadora.gamma",
            class_name="Calculadora",
            file_path=file_path,
            source_code="def gamma(self): return 3",
        ),
    ]


def test_class_with_three_methods_filters_container_class() -> None:
    result = filter_symbols(_class_with_three_methods())

    kept_names = {s.qualified_name for s in result.kept}
    assert kept_names == {
        "Calculadora.alpha",
        "Calculadora.beta",
        "Calculadora.gamma",
    }
    assert result.stats.removed_container_class == 1
    assert result.stats.extracted_total == 4
    assert result.stats.filtered_total == 1


def test_top_level_function_stays_eligible() -> None:
    symbols = _class_with_three_methods() + [
        _symbol(name="soma", source_code="def soma(a, b): return a + b"),
    ]
    result = filter_symbols(symbols)

    assert any(s.qualified_name == "soma" for s in result.kept)


def test_empty_class_does_not_error() -> None:
    symbols = [
        _symbol(
            symbol_type="class",
            name="Empty",
            source_code="class Empty:\n    pass\n",
        ),
    ]
    result = filter_symbols(symbols)

    assert result.kept == []
    assert result.stats.removed_container_class == 0


def test_init_and_public_methods_no_class_duplication() -> None:
    file_path = "service.py"
    symbols = [
        _symbol(
            symbol_type="class",
            name="Service",
            file_path=file_path,
            source_code=(
                "class Service:\n"
                "    def __init__(self, x):\n"
                "        self.x = x\n"
                "    def run(self):\n"
                "        return self.x\n"
            ),
        ),
        _symbol(
            symbol_type="method",
            name="__init__",
            qualified_name="Service.__init__",
            class_name="Service",
            file_path=file_path,
            source_code="def __init__(self, x):\n        self.x = x",
        ),
        _symbol(
            symbol_type="method",
            name="run",
            qualified_name="Service.run",
            class_name="Service",
            file_path=file_path,
            source_code="def run(self):\n        return self.x",
        ),
    ]

    result = filter_symbols(symbols)
    kept_qnames = {s.qualified_name for s in result.kept}

    assert "Service" not in kept_qnames
    assert kept_qnames == {"Service.__init__", "Service.run"}
    assert result.stats.removed_container_class == 1


def test_qualified_names_remain_stable() -> None:
    result = filter_symbols(_class_with_three_methods())

    assert sorted(s.qualified_name for s in result.kept) == [
        "Calculadora.alpha",
        "Calculadora.beta",
        "Calculadora.gamma",
    ]


def test_class_with_executable_body_without_methods_is_kept() -> None:
    symbols = [
        _symbol(
            symbol_type="class",
            name="Defaults",
            source_code="class Defaults:\n    TIMEOUT = 30\n",
        ),
    ]

    result = filter_symbols(symbols)
    assert len(result.kept) == 1
    assert result.kept[0].qualified_name == "Defaults"
    assert result.stats.removed_container_class == 0


def test_extraction_integration(tmp_path: Path) -> None:
    source = tmp_path / "module.py"
    source.write_text(
        "class Box:\n"
        "    def open(self):\n"
        "        return True\n"
        "    def close(self):\n"
        "        return False\n"
        "\n"
        "def ping():\n"
        "    return 'pong'\n",
        encoding="utf-8",
    )

    extracted = list(parse_file_symbols(str(source)))
    result = filter_symbols(extracted)

    kept_qnames = {s.qualified_name for s in result.kept}
    assert "Box" not in kept_qnames
    assert kept_qnames == {"Box.open", "Box.close", "ping"}


def test_exemplo_fixture_fewer_llm_targets(tmp_path: Path) -> None:
    """Cada símbolo elegível dispara ao menos uma chamada LLM de geração."""
    fixture = tmp_path / "exemplo.py"
    fixture.write_text(
        "def soma(a, b):\n"
        "    return a + b\n"
        "\n"
        "class Calculadora:\n"
        "    def multiplica(self, a, b):\n"
        "        return a * b\n"
        "    def divide(self, a, b):\n"
        "        return a / b\n"
        "    def potencia(self, a, b):\n"
        "        return a ** b\n",
        encoding="utf-8",
    )

    extracted = list(parse_file_symbols(str(fixture)))
    result = filter_symbols(extracted)

    assert len(extracted) == 5
    assert len(result.kept) == 4
    assert result.stats.removed_container_class == 1
    assert not any(s.symbol_type == "class" for s in result.kept)
    assert {s.qualified_name for s in result.kept} == {
        "soma",
        "Calculadora.multiplica",
        "Calculadora.divide",
        "Calculadora.potencia",
    }
