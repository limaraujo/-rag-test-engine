import ast
from textwrap import dedent

from ingest.collectors.branches import BranchCollector
from ingest.collectors.dependency_collector import DependencyCollector
from ingest.collectors.exceptions import ExceptionCollector
from ingest.collectors.imports import ImportCollector
from ingest.heuristics.edge_cases import EdgeCaseInferer


def test_import_collector_collects_imports() -> None:
    code = dedent(
        """
        import os
        import pathlib as pl
        from typing import List, Optional
        from . import utils
        """
    )
    tree = ast.parse(code)

    collector = ImportCollector()
    collector.visit(tree)

    assert collector.imports == {
        "os",
        "pathlib",
        "typing.List",
        "typing.Optional",
        "utils",
    }


def test_dependency_collector_ignores_builtins() -> None:
    code = dedent(
        """
        def run(items):
            len(items)
            max(1, 2)
        """
    )
    tree = ast.parse(code)

    collector = DependencyCollector()
    collector.visit(tree)

    assert collector.dependencies == set()


def test_dependency_collector_rebuilds_chained_calls() -> None:
    code = dedent(
        """
        def run(self, user, response):
            requests.get("https://example.com")
            Path(__file__).resolve()
            self.repo.save()
            user.profile.update()
            response.json()
        """
    )
    tree = ast.parse(code)

    collector = DependencyCollector()
    collector.visit(tree)

    assert collector.dependencies == {
        "requests.get",
        "Path.resolve",
        "self.repo.save",
        "user.profile.update",
        "response.json",
    }


def test_exception_collector_extracts_raise_and_except() -> None:
    code = dedent(
        """
        def run():
            raise ValueError()
            raise fastapi.HTTPException()
            try:
                pass
            except ValueError:
                pass
            except (ValueError, TypeError):
                pass
            except (
                requests.Timeout,
                requests.ConnectionError,
            ):
                pass
        """
    )
    tree = ast.parse(code)

    collector = ExceptionCollector()
    collector.visit(tree)

    assert collector.exceptions == {
        "ValueError",
        "fastapi.HTTPException",
        "TypeError",
        "requests.Timeout",
        "requests.ConnectionError",
    }


def test_branch_collector_counts_branches() -> None:
    code = dedent(
        """
        def run(x):
            if x > 0:
                pass
            elif x < 0:
                pass
            for i in range(3):
                pass
            while x < 10:
                x += 1
            try:
                x / 2
            except ZeroDivisionError:
                pass
            match x:
                case 1:
                    pass
                case _:
                    pass
        """
    )
    tree = ast.parse(code)

    collector = BranchCollector()
    collector.visit(tree)

    assert collector.branches == 6


def test_branch_collector_counts_if_elif_separately() -> None:
    code = dedent(
        """
        def run(x):
            if x > 0:
                pass
            elif x < 0:
                pass
        """
    )
    tree = ast.parse(code)

    collector = BranchCollector()
    collector.visit(tree)

    assert collector.branches == 2


def test_edge_case_inferer_is_conservative() -> None:
    code = dedent(
        """
        def run():
            root = Path(__file__).resolve()
            total = sum([1, 2, 3])
            return root, total
        """
    )
    tree = ast.parse(code)

    inferer = EdgeCaseInferer()
    inferer.visit(tree)

    assert inferer.edge_cases == set()


def test_edge_case_inferer_detects_evidence() -> None:
    code = dedent(
        """
        def run(items, value):
            if len(items) == 0:
                return None
            try:
                value = value / 0
                return items[0]
            except IndexError:
                raise ValueError("bad")
            except KeyError:
                pass
        """
    )
    tree = ast.parse(code)

    inferer = EdgeCaseInferer()
    inferer.visit(tree)

    assert inferer.edge_cases == {
        "division_by_zero",
        "index_out_of_bounds",
        "empty_collection",
        "invalid_input",
        "missing_key",
    }
