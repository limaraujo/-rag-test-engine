import json
from textwrap import dedent

import pytest

from parsers.source.call_graph import (
    CallGraph,
    CallGraphBuilder,
    CallGraphNode,
    CodeSymbol,
)
from parsers.source.models.ExtractedSymbol import ExtractedSymbol
from tests.conftest import make_symbol


def _symbol(
    name: str,
    *,
    source_code: str,
    qualified_name: str | None = None,
    symbol_type: str = "function",
    class_name: str | None = None,
    file_path: str | None = None,
    imports: list[str] | None = None,
) -> ExtractedSymbol:
    return ExtractedSymbol(
        symbol_type=symbol_type,
        name=name,
        qualified_name=qualified_name or (
            f"{class_name}.{name}" if class_name else name
        ),
        class_name=class_name,
        file_path=file_path or f"src/{name}.py",
        source_code=source_code,
        imports=imports or [],
        dependencies=[],
        exceptions=[],
        decorators=[],
        docstring=None,
        branches=0,
        edge_cases=[],
    )


def _order_symbols() -> list[CodeSymbol]:
    return [
        make_symbol(
            "process_order",
            source_code=dedent(
                """
                def process_order(user, order):
                    validate_user(user)
                    discount = calculate_discount(order)
                    return save_order(order, discount)
                """
            ),
        ),
        make_symbol(
            "validate_user",
            source_code=dedent(
                """
                def validate_user(user):
                    if not user:
                        raise ValueError("invalid")
                """
            ),
        ),
        make_symbol(
            "calculate_discount",
            source_code=dedent(
                """
                def calculate_discount(order):
                    return order.total * 0.1
                """
            ),
        ),
        make_symbol(
            "save_order",
            source_code=dedent(
                """
                def save_order(order, discount):
                    return order.id
                """
            ),
        ),
    ]


def test_build_creates_expected_call_tree() -> None:
    builder = CallGraphBuilder()
    graph = builder.build(_order_symbols())

    assert graph.nodes["process_order"].calls == [
        "calculate_discount",
        "save_order",
        "validate_user",
    ]
    assert graph.nodes["validate_user"].calls == []
    assert graph.nodes["validate_user"].called_by == ["process_order"]
    assert graph.nodes["calculate_discount"].called_by == ["process_order"]
    assert graph.nodes["save_order"].called_by == ["process_order"]

    tree = builder.format_tree("process_order")
    assert tree == dedent(
        """\
        process_order
         ├── calculate_discount
         ├── save_order
         └── validate_user"""
    )


def test_get_dependencies_and_dependents() -> None:
    builder = CallGraphBuilder()
    builder.build(_order_symbols())

    assert builder.get_dependencies("process_order") == [
        "calculate_discount",
        "save_order",
        "validate_user",
    ]
    assert builder.get_dependencies("validate_user") == []
    assert builder.get_dependents("validate_user") == ["process_order"]
    assert builder.get_dependents("missing") == []


def test_builder_requires_build_before_query() -> None:
    builder = CallGraphBuilder()

    with pytest.raises(RuntimeError, match="has not been built"):
        builder.get_dependencies("process_order")


def test_resolves_method_calls_via_self() -> None:
    symbols = [
        make_symbol(
            "process",
            source_code=dedent(
                """
                class OrderService:
                    def process(self, order):
                        self.validate(order)
                        return self.persist(order)
                """
            ),
            symbol_type="method",
            class_name="OrderService",
        ),
        make_symbol(
            "validate",
            source_code=dedent(
                """
                class OrderService:
                    def validate(self, order):
                        return order.is_valid()
                """
            ),
            symbol_type="method",
            class_name="OrderService",
        ),
        make_symbol(
            "persist",
            source_code=dedent(
                """
                class OrderService:
                    def persist(self, order):
                        return order.id
                """
            ),
            symbol_type="method",
            class_name="OrderService",
        ),
    ]

    graph = CallGraphBuilder().build(symbols)

    assert graph.nodes["OrderService.process"].calls == [
        "OrderService.persist",
        "OrderService.validate",
    ]


def test_resolves_class_method_calls() -> None:
    symbols = [
        make_symbol(
            "run",
            source_code=dedent(
                """
                def run():
                    return Calculator.add(1, 2)
                """
            ),
        ),
        make_symbol(
            "add",
            source_code=dedent(
                """
                class Calculator:
                    @staticmethod
                    def add(a, b):
                        return a + b
                """
            ),
            symbol_type="method",
            class_name="Calculator",
        ),
        make_symbol(
            "Calculator",
            source_code=dedent(
                """
                class Calculator:
                    @staticmethod
                    def add(a, b):
                        return a + b
                """
            ),
            symbol_type="class",
        ),
    ]

    graph = CallGraphBuilder().build(symbols)

    assert graph.nodes["run"].calls == ["Calculator.add"]


def test_prefers_same_file_for_ambiguous_simple_names() -> None:
    symbols = [
        _symbol(
            "caller",
            source_code=dedent(
                """
                def caller():
                    return helper()
                """
            ),
            file_path="src/a/module.py",
        ),
        _symbol(
            "helper",
            source_code="def helper(): return 1",
            file_path="src/a/module.py",
        ),
        _symbol(
            "helper",
            qualified_name="remote.helper",
            source_code="def helper(): return 2",
            file_path="src/b/module.py",
        ),
    ]

    graph = CallGraphBuilder().build(symbols)

    assert graph.nodes["caller"].calls == ["helper"]
    assert graph.nodes["helper"].called_by == ["caller"]
    assert graph.nodes["remote.helper"].called_by == []


def test_ignores_builtin_and_external_calls() -> None:
    symbols = [
        _symbol(
            "run",
            source_code=dedent(
                """
                def run(items):
                    len(items)
                    print("ok")
                    requests.get("/")
                    return helper()
                """
            ),
            imports=["requests"],
        ),
        _symbol("helper", source_code="def helper(): pass"),
    ]

    graph = CallGraphBuilder().build(symbols)

    assert graph.nodes["run"].calls == ["helper"]


def test_does_not_include_self_references() -> None:
    symbols = [
        make_symbol(
            "recurse",
            source_code=dedent(
                """
                def recurse(n):
                    if n <= 0:
                        return 0
                    return recurse(n - 1)
                """
            ),
        )
    ]

    graph = CallGraphBuilder().build(symbols)

    assert graph.nodes["recurse"].calls == []


def test_skips_non_callable_symbols_as_nodes() -> None:
    symbols = [
        make_symbol(
            "MyClass",
            source_code="class MyClass: pass",
            symbol_type="class",
        ),
        make_symbol("run", source_code="def run(): pass"),
    ]

    graph = CallGraphBuilder().build(symbols)

    assert "MyClass" not in graph.nodes
    assert "run" in graph.nodes


def test_export_to_json() -> None:
    builder = CallGraphBuilder()
    builder.build(_order_symbols())

    payload = json.loads(builder.to_json())

    assert payload["process_order"] == {
        "qualified_name": "process_order",
        "calls": ["calculate_discount", "save_order", "validate_user"],
        "called_by": [],
    }
    assert payload["validate_user"]["called_by"] == ["process_order"]


def test_call_graph_to_dict_and_node_dataclass() -> None:
    node = CallGraphNode(
        qualified_name="foo",
        calls=["bar"],
        called_by=["baz"],
    )
    graph = CallGraph(nodes={"foo": node})

    assert graph.to_dict() == {
        "foo": {
            "qualified_name": "foo",
            "calls": ["bar"],
            "called_by": ["baz"],
        }
    }
    assert json.loads(graph.to_json()) == graph.to_dict()


def test_resolves_imported_call_with_root(tmp_path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    service_file = root / "pkg" / "service.py"
    helper_file = root / "pkg" / "helpers.py"
    service_file.parent.mkdir(parents=True)
    helper_file.write_text(
        dedent(
            """
            def format_name(value):
                return value
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    service_file.write_text(
        dedent(
            """
            from pkg.helpers import format_name

            def run(value):
                return format_name(value)
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )

    symbols = [
        _symbol(
            "run",
            source_code=service_file.read_text(encoding="utf-8"),
            file_path=str(service_file),
            imports=["pkg.helpers.format_name"],
        ),
        _symbol(
            "format_name",
            source_code=helper_file.read_text(encoding="utf-8"),
            file_path=str(helper_file),
        ),
    ]

    graph = CallGraphBuilder(str(root)).build(symbols)

    assert graph.nodes["run"].calls == ["format_name"]


def test_parse_repository_graphs_integration(tmp_path) -> None:
    root = tmp_path / "project"
    module = root / "orders.py"
    root.mkdir()
    module.write_text(
        dedent(
            """
            def process_order():
                return validate_user()

            def validate_user():
                return True
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )

    from parsers.source.parser import parse_repository_graphs

    symbols, call_graph, dependency_graph = parse_repository_graphs(str(root))

    assert len(symbols) == 2
    assert call_graph.nodes["process_order"].calls == ["validate_user"]
    assert "orders" in dependency_graph.nodes


def test_handles_invalid_source_code_gracefully() -> None:
    symbols = [
        make_symbol("broken", source_code="def broken(:"),
        make_symbol("ok", source_code="def ok(): broken_ok()"),
        make_symbol("broken_ok", source_code="def broken_ok(): pass"),
    ]

    graph = CallGraphBuilder().build(symbols)

    assert graph.nodes["broken"].calls == []
    assert graph.nodes["ok"].calls == ["broken_ok"]
