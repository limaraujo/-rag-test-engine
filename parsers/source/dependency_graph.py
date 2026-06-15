from __future__ import annotations

import ast
import json
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

from parsers.source.import_resolver import ImportResolver, module_name_from_path
from parsers.source.path_filters import scan_python_files
from parsers.source.text_utils import read_source_text


@dataclass
class DependencyNode:
    qualified_name: str
    dependencies: list[str] = field(default_factory=list)


@dataclass
class DependencyGraph:
    nodes: dict[str, DependencyNode] = field(default_factory=dict)

    def to_dict(self) -> dict[str, dict[str, list[str]]]:
        return {
            name: {
                "qualified_name": node.qualified_name,
                "dependencies": node.dependencies,
            }
            for name, node in self.nodes.items()
        }

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class _ClassDependencyCollector(ast.NodeVisitor):
    """Collect inheritance and composition dependencies for a class body."""

    def __init__(self, resolver: ImportResolver, module_name: str) -> None:
        self.resolver = resolver
        self.module_name = module_name
        self.dependencies: set[str] = set()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.annotation is not None:
            self._add_reference(node.annotation)

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Call):
            self._add_reference(node.value.func)
        for target in node.targets:
            if isinstance(target, ast.AnnAssign):
                continue
            if isinstance(target, ast.Attribute) and isinstance(
                target.value, ast.Name
            ):
                if target.value.id == "self" and isinstance(node.value, ast.Call):
                    self._add_reference(node.value.func)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name != "__init__":
            return
        for child in node.body:
            if isinstance(child, ast.Assign):
                self.visit_Assign(child)
            elif isinstance(child, ast.AnnAssign):
                self.visit_AnnAssign(child)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if node.name != "__init__":
            return
        for child in node.body:
            if isinstance(child, ast.Assign):
                self.visit_Assign(child)
            elif isinstance(child, ast.AnnAssign):
                self.visit_AnnAssign(child)

    def _add_reference(self, node: ast.AST) -> None:
        resolved = self.resolver.resolve_reference(node)
        if resolved:
            self.dependencies.add(resolved)


class _ModuleAstAnalyzer:
    """Analyze a module AST and extract module/class dependency nodes."""

    def __init__(self, module_name: str, local_modules: set[str]) -> None:
        self.module_name = module_name
        self.local_modules = local_modules
        self.resolver = ImportResolver(module_name, local_modules)
        self.module_dependencies: set[str] = set()
        self.class_dependencies: dict[str, set[str]] = {}

    def analyze(self, tree: ast.AST) -> None:
        self._collect_imports(tree)
        self._collect_classes(tree, class_prefix="")

    def _collect_imports(self, tree: ast.AST) -> None:
        for node in tree.body:
            if isinstance(node, ast.Import):
                self.module_dependencies.update(
                    self.resolver.register_import(node)
                )
            elif isinstance(node, ast.ImportFrom):
                self.module_dependencies.update(
                    self.resolver.register_import_from(node)
                )

    def _collect_classes(self, tree: ast.AST, *, class_prefix: str) -> None:
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue

            qualified_name = (
                f"{self.module_name}.{class_prefix}{node.name}"
                if class_prefix
                else f"{self.module_name}.{node.name}"
            )
            dependencies: set[str] = set()

            for base in node.bases:
                resolved = self.resolver.resolve_reference(base)
                if resolved:
                    dependencies.add(resolved)

            collector = _ClassDependencyCollector(self.resolver, self.module_name)
            for child in node.body:
                if isinstance(child, ast.ClassDef):
                    continue
                collector.visit(child)

            dependencies.update(collector.dependencies)
            self.class_dependencies[qualified_name] = dependencies

            nested_prefix = (
                f"{class_prefix}{node.name}."
                if class_prefix
                else f"{node.name}."
            )
            self._collect_nested_classes(node, prefix=nested_prefix)

    def _collect_nested_classes(self, class_node: ast.ClassDef, *, prefix: str) -> None:
        for node in class_node.body:
            if not isinstance(node, ast.ClassDef):
                continue

            qualified_name = f"{self.module_name}.{prefix}{node.name}"
            dependencies: set[str] = set()

            for base in node.bases:
                resolved = self.resolver.resolve_reference(base)
                if resolved:
                    dependencies.add(resolved)

            collector = _ClassDependencyCollector(self.resolver, self.module_name)
            for child in node.body:
                if isinstance(child, ast.ClassDef):
                    continue
                collector.visit(child)

            dependencies.update(collector.dependencies)
            self.class_dependencies[qualified_name] = dependencies
            self._collect_nested_classes(node, prefix=f"{prefix}{node.name}.")


class DependencyGraphBuilder:
    """Build and query a dependency graph from Python source files using AST."""

    def __init__(self, root: str) -> None:
        self.root = Path(root)
        self._graph: DependencyGraph | None = None
        self._local_entities: set[str] = set()

    def build(self) -> DependencyGraph:
        python_files = self._discover_python_files()
        local_modules = {
            module_name_from_path(self.root, path) for path in python_files
        }

        graph = DependencyGraph()
        local_entities: set[str] = set(local_modules)

        for path in python_files:
            module_name = module_name_from_path(self.root, path)
            graph.nodes.setdefault(
                module_name,
                DependencyNode(qualified_name=module_name),
            )

            try:
                source = read_source_text(path)
                tree = ast.parse(source, filename=str(path))
            except (OSError, SyntaxError):
                continue

            analyzer = _ModuleAstAnalyzer(module_name, local_modules)
            analyzer.analyze(tree)

            module_node = graph.nodes[module_name]
            module_node.dependencies = sorted(analyzer.module_dependencies)

            for class_name, dependencies in analyzer.class_dependencies.items():
                graph.nodes[class_name] = DependencyNode(
                    qualified_name=class_name,
                    dependencies=sorted(dependencies),
                )
                local_entities.add(class_name)

        self._local_entities = local_entities
        self._graph = graph
        return graph

    def find_transitive_dependencies(self, qualified_name: str) -> list[str]:
        graph = self._require_graph()
        visited: set[str] = set()
        queue: deque[str] = deque()

        for dependency in graph.nodes.get(
            qualified_name, DependencyNode(qualified_name)
        ).dependencies:
            if dependency not in visited:
                visited.add(dependency)
                queue.append(dependency)

        while queue:
            current = queue.popleft()
            for dependency in graph.nodes.get(
                current, DependencyNode(current)
            ).dependencies:
                if dependency not in visited:
                    visited.add(dependency)
                    queue.append(dependency)

        return sorted(visited)

    def find_local_dependencies(self, qualified_name: str) -> list[str]:
        graph = self._require_graph()
        node = graph.nodes.get(qualified_name)
        if node is None:
            return []
        return sorted(
            dependency
            for dependency in node.dependencies
            if dependency in self._local_entities
        )

    def to_dict(self) -> dict[str, dict[str, list[str]]]:
        return self._require_graph().to_dict()

    def to_json(self, *, indent: int = 2) -> str:
        return self._require_graph().to_json(indent=indent)

    def _require_graph(self) -> DependencyGraph:
        if self._graph is None:
            raise RuntimeError(
                "Dependency graph has not been built yet. Call build() first."
            )
        return self._graph

    def _discover_python_files(self) -> list[Path]:
        return list(scan_python_files(self.root).files)
