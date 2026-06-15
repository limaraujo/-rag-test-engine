import json
from textwrap import dedent

import pytest

from parsers.source.dependency_graph import (
    DependencyGraph,
    DependencyGraphBuilder,
    DependencyNode,
)


def _write(path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def test_absolute_imports(tmp_path) -> None:
    root = tmp_path / "project"
    _write(
        root / "pkg" / "service.py",
        """
        import pkg.repository
        from pkg.models import Order

        class OrderService:
            pass
        """,
    )
    _write(root / "pkg" / "repository.py", "class Repository: pass")
    _write(root / "pkg" / "models.py", "class Order: pass")
    _write(root / "pkg" / "__init__.py", "")

    graph = DependencyGraphBuilder(str(root)).build()

    assert graph.nodes["pkg.service"].dependencies == [
        "pkg.models",
        "pkg.models.Order",
        "pkg.repository",
    ]


def test_relative_imports(tmp_path) -> None:
    root = tmp_path / "project"
    _write(
        root / "pkg" / "api" / "routes.py",
        """
        from ..utils.helpers import format_name
        from . import schemas

        def list_items():
            return format_name("item")
        """,
    )
    _write(
        root / "pkg" / "api" / "schemas.py",
        """
        class ItemSchema:
            pass
        """,
    )
    _write(root / "pkg" / "api" / "__init__.py", "")
    _write(
        root / "pkg" / "utils" / "helpers.py",
        """
        def format_name(value):
            return value
        """,
    )
    _write(root / "pkg" / "utils" / "__init__.py", "")
    _write(root / "pkg" / "__init__.py", "")

    graph = DependencyGraphBuilder(str(root)).build()

    assert graph.nodes["pkg.api.routes"].dependencies == [
        "pkg.api",
        "pkg.api.schemas",
        "pkg.utils.helpers",
        "pkg.utils.helpers.format_name",
    ]


def test_inherited_classes(tmp_path) -> None:
    root = tmp_path / "project"
    _write(
        root / "pkg" / "base.py",
        """
        class Entity:
            pass
        """,
    )
    _write(
        root / "pkg" / "models.py",
        """
        from pkg.base import Entity

        class User(Entity):
            pass
        """,
    )
    _write(root / "pkg" / "__init__.py", "")

    graph = DependencyGraphBuilder(str(root)).build()

    assert graph.nodes["pkg.models"].dependencies == [
        "pkg.base",
        "pkg.base.Entity",
    ]
    assert graph.nodes["pkg.models.User"].dependencies == ["pkg.base.Entity"]


def test_nested_modules_and_classes(tmp_path) -> None:
    root = tmp_path / "project"
    _write(
        root / "pkg" / "outer" / "container.py",
        """
        from pkg.outer.inner.worker import Worker

        class Container:
            class Engine:
                def __init__(self):
                    self.worker = Worker()
        """,
    )
    _write(
        root / "pkg" / "outer" / "inner" / "worker.py",
        """
        class Worker:
            pass
        """,
    )
    _write(root / "pkg" / "outer" / "inner" / "__init__.py", "")
    _write(root / "pkg" / "outer" / "__init__.py", "")
    _write(root / "pkg" / "__init__.py", "")

    graph = DependencyGraphBuilder(str(root)).build()

    assert graph.nodes["pkg.outer.container"].dependencies == [
        "pkg.outer.inner.worker",
        "pkg.outer.inner.worker.Worker",
    ]
    assert graph.nodes["pkg.outer.container.Container.Engine"].dependencies == [
        "pkg.outer.inner.worker.Worker",
    ]
    assert "pkg.outer.inner.worker" in graph.nodes
    assert "pkg.outer.inner.worker.Worker" in graph.nodes


def test_find_local_dependencies(tmp_path) -> None:
    root = tmp_path / "project"
    _write(
        root / "app" / "main.py",
        """
        import json
        from app.core import Service

        class App:
            pass
        """,
    )
    _write(
        root / "app" / "core.py",
        """
        class Service:
            pass
        """,
    )
    _write(root / "app" / "__init__.py", "")

    builder = DependencyGraphBuilder(str(root))
    builder.build()

    assert builder.find_local_dependencies("app.main") == [
        "app.core",
        "app.core.Service",
    ]


def test_find_transitive_dependencies(tmp_path) -> None:
    root = tmp_path / "project"
    _write(
        root / "a.py",
        """
        import b
        """,
    )
    _write(
        root / "b.py",
        """
        import c
        """,
    )
    _write(root / "c.py", "VALUE = 1")

    builder = DependencyGraphBuilder(str(root))
    builder.build()

    assert builder.find_transitive_dependencies("a") == ["b", "c"]


def test_export_to_json(tmp_path) -> None:
    root = tmp_path / "project"
    _write(root / "mod.py", "import os")

    builder = DependencyGraphBuilder(str(root))
    builder.build()

    payload = json.loads(builder.to_json())

    assert payload["mod"] == {
        "qualified_name": "mod",
        "dependencies": ["os"],
    }


def test_dependency_graph_dataclass_helpers() -> None:
    node = DependencyNode(
        qualified_name="pkg.mod",
        dependencies=["pkg.other"],
    )
    graph = DependencyGraph(nodes={"pkg.mod": node})

    assert graph.to_dict() == {
        "pkg.mod": {
            "qualified_name": "pkg.mod",
            "dependencies": ["pkg.other"],
        }
    }
    assert json.loads(graph.to_json()) == graph.to_dict()


def test_builder_requires_build_before_query() -> None:
    builder = DependencyGraphBuilder(".")

    with pytest.raises(RuntimeError, match="has not been built"):
        builder.find_local_dependencies("anything")


def test_parse_repository_graphs_exposes_dependency_graph(tmp_path) -> None:
    root = tmp_path / "project"
    _write(root / "pkg" / "mod.py", "import os")
    _write(root / "pkg" / "__init__.py", "")

    from parsers.source.parser import parse_repository_graphs

    _, _, dependency_graph = parse_repository_graphs(str(root))
    assert "pkg.mod" in dependency_graph.nodes
