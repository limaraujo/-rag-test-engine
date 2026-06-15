from __future__ import annotations

import ast
import json
from dataclasses import dataclass, field
from pathlib import Path

from parsers.source.collectors.dependency_collector import DependencyCollector
from parsers.source.import_resolver import ImportResolver, module_name_from_path
from parsers.source.models.ExtractedSymbol import ExtractedSymbol
from parsers.source.text_utils import read_source_text

CodeSymbol = ExtractedSymbol

CALLABLE_SYMBOL_TYPES = frozenset({"function", "method"})


@dataclass
class CallGraphNode:
    qualified_name: str
    calls: list[str] = field(default_factory=list)
    called_by: list[str] = field(default_factory=list)


@dataclass
class CallGraph:
    nodes: dict[str, CallGraphNode] = field(default_factory=dict)

    def to_dict(self) -> dict[str, dict[str, list[str]]]:
        return {
            name: {
                "qualified_name": node.qualified_name,
                "calls": node.calls,
                "called_by": node.called_by,
            }
            for name, node in self.nodes.items()
        }

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class _SymbolIndex:
    """Index project symbols and resolve internal call targets."""

    def __init__(
        self,
        symbols: list[CodeSymbol],
        *,
        root: Path | None,
    ) -> None:
        self._by_qualified: dict[str, CodeSymbol] = {}
        self._by_simple_name: dict[str, list[str]] = {}
        self._by_file: dict[str, list[str]] = {}
        self._class_methods: dict[str, dict[str, str]] = {}
        self._classes: set[str] = set()
        self._module_to_file: dict[str, str] = {}
        self._file_resolvers: dict[str, ImportResolver] = {}
        self._fallback_resolvers: dict[str, ImportResolver] = {}

        for symbol in symbols:
            self._by_qualified[symbol.qualified_name] = symbol

            if symbol.symbol_type == "class":
                self._classes.add(symbol.qualified_name)
                self._classes.add(symbol.name)

            if symbol.symbol_type in CALLABLE_SYMBOL_TYPES:
                self._by_simple_name.setdefault(symbol.name, []).append(
                    symbol.qualified_name
                )
                self._by_file.setdefault(symbol.file_path, []).append(
                    symbol.qualified_name
                )

                if symbol.class_name:
                    self._class_methods.setdefault(symbol.class_name, {})[
                        symbol.name
                    ] = symbol.qualified_name

        self._build_resolvers(symbols, root=root)

    def _build_resolvers(
        self,
        symbols: list[CodeSymbol],
        *,
        root: Path | None,
    ) -> None:
        files = {symbol.file_path for symbol in symbols}
        local_modules: set[str] = set()

        if root is not None:
            for file_path in files:
                try:
                    local_modules.add(
                        module_name_from_path(root, Path(file_path))
                    )
                except ValueError:
                    continue

            for file_path in files:
                try:
                    module_name = module_name_from_path(root, Path(file_path))
                    self._module_to_file[module_name] = file_path
                    source = read_source_text(file_path)
                    tree = ast.parse(source, filename=file_path)
                    resolver = ImportResolver(module_name, local_modules)
                    resolver.populate_from_tree(tree)
                    self._file_resolvers[file_path] = resolver
                except (OSError, SyntaxError, ValueError):
                    continue

        fallback_imports: dict[str, list[str]] = {}
        for symbol in symbols:
            if symbol.file_path in self._file_resolvers:
                continue
            fallback_imports.setdefault(symbol.file_path, []).extend(symbol.imports)

        for file_path, imports in fallback_imports.items():
            module_name = self._module_to_file.get(file_path, file_path)
            self._fallback_resolvers[file_path] = ImportResolver.from_import_strings(
                module_name,
                sorted(set(imports)),
            )

    def _resolver_for(self, file_path: str) -> ImportResolver | None:
        if file_path in self._file_resolvers:
            return self._file_resolvers[file_path]
        return self._fallback_resolvers.get(file_path)

    def resolve(
        self,
        raw_call: str,
        *,
        file_path: str,
        class_name: str | None,
    ) -> str | None:
        if raw_call in self._by_qualified:
            return raw_call

        if raw_call == "self" and class_name:
            return None

        if raw_call.startswith("self."):
            method_name = raw_call.removeprefix("self.")
            if class_name and method_name in self._class_methods.get(
                class_name, {}
            ):
                return self._class_methods[class_name][method_name]
            return None

        resolver = self._resolver_for(file_path)
        if resolver is not None:
            if "." in raw_call:
                root_name, _, member = raw_call.partition(".")
                expanded_root = resolver.resolve_name(root_name)
                if expanded_root != root_name:
                    module_match = self._resolve_module_reference(
                        f"{expanded_root}.{member}"
                    )
                    if module_match:
                        return module_match
            else:
                expanded = resolver.resolve_name(raw_call)
                if expanded != raw_call:
                    module_match = self._resolve_module_reference(expanded)
                    if module_match:
                        return module_match

        if "." in raw_call:
            return self._resolve_qualified(raw_call, file_path=file_path)

        return self._resolve_simple(raw_call, file_path=file_path)

    def _resolve_module_reference(self, reference: str) -> str | None:
        if reference in self._by_qualified:
            return reference

        parts = reference.split(".")
        for split in range(len(parts) - 1, 0, -1):
            module_path = ".".join(parts[:split])
            remainder = ".".join(parts[split:])
            file_path = self._module_to_file.get(module_path)
            if file_path is None:
                continue

            if remainder in self._by_qualified:
                return remainder

            remainder_name = remainder.split(".")[-1]
            file_candidates = [
                qualified
                for qualified in self._by_file.get(file_path, [])
                if self._by_qualified[qualified].name == remainder_name
            ]
            if len(file_candidates) == 1:
                return file_candidates[0]

        return None

    def _resolve_qualified(self, raw_call: str, *, file_path: str) -> str | None:
        if raw_call in self._by_qualified:
            return raw_call

        module_match = self._resolve_module_reference(raw_call)
        if module_match:
            return module_match

        root, _, member = raw_call.partition(".")
        if root in self._classes:
            candidate = f"{root}.{member}"
            if candidate in self._by_qualified:
                return candidate

        resolver = self._resolver_for(file_path)
        if resolver is not None:
            expanded_root = resolver.resolve_name(root)
            if expanded_root != root:
                module_match = self._resolve_module_reference(
                    f"{expanded_root}.{member}"
                )
                if module_match:
                    return module_match

        return None

    def _resolve_simple(self, name: str, *, file_path: str) -> str | None:
        file_candidates = [
            qualified
            for qualified in self._by_file.get(file_path, [])
            if self._by_qualified[qualified].name == name
        ]
        if len(file_candidates) == 1:
            return file_candidates[0]

        project_candidates = self._by_simple_name.get(name, [])
        if len(project_candidates) == 1:
            return project_candidates[0]

        resolver = self._resolver_for(file_path)
        if resolver is not None:
            expanded = resolver.resolve_name(name)
            if expanded != name:
                module_match = self._resolve_module_reference(expanded)
                if module_match:
                    return module_match

        return None


class CallGraphBuilder:
    """Build and query a call graph from extracted code symbols."""

    def __init__(self, root: str | None = None) -> None:
        self.root = Path(root).resolve() if root is not None else None
        self._graph: CallGraph | None = None

    def build(self, symbols: list[CodeSymbol]) -> CallGraph:
        index = _SymbolIndex(symbols, root=self.root)
        graph = CallGraph()

        callable_symbols = [
            symbol
            for symbol in symbols
            if symbol.symbol_type in CALLABLE_SYMBOL_TYPES
        ]

        for symbol in callable_symbols:
            graph.nodes[symbol.qualified_name] = CallGraphNode(
                qualified_name=symbol.qualified_name
            )

        for symbol in callable_symbols:
            resolved_calls = self._extract_resolved_calls(symbol, index)
            node = graph.nodes[symbol.qualified_name]
            node.calls = sorted(resolved_calls)

            for callee in node.calls:
                if callee in graph.nodes:
                    graph.nodes[callee].called_by.append(symbol.qualified_name)

        for node in graph.nodes.values():
            node.called_by = sorted(set(node.called_by))

        self._graph = graph
        return graph

    def get_dependencies(self, symbol_name: str) -> list[str]:
        graph = self._require_graph()
        node = graph.nodes.get(symbol_name)
        if node is None:
            return []
        return list(node.calls)

    def get_dependents(self, symbol_name: str) -> list[str]:
        graph = self._require_graph()
        node = graph.nodes.get(symbol_name)
        if node is None:
            return []
        return list(node.called_by)

    def to_json(self, *, indent: int = 2) -> str:
        return self._require_graph().to_json(indent=indent)

    def to_dict(self) -> dict[str, dict[str, list[str]]]:
        return self._require_graph().to_dict()

    def format_tree(self, root: str) -> str:
        graph = self._require_graph()
        if root not in graph.nodes:
            return root

        lines = [root]

        def append_children(name: str, prefix: str) -> None:
            calls = graph.nodes[name].calls
            for index, child in enumerate(calls):
                is_last = index == len(calls) - 1
                connector = " └── " if is_last else " ├── "
                lines.append(f"{prefix}{connector}{child}")
                if child in graph.nodes:
                    extension = "    " if is_last else " │   "
                    append_children(child, prefix + extension)

        append_children(root, "")
        return "\n".join(lines)

    def _require_graph(self) -> CallGraph:
        if self._graph is None:
            raise RuntimeError("Call graph has not been built yet. Call build() first.")
        return self._graph

    @staticmethod
    def _extract_resolved_calls(
        symbol: CodeSymbol,
        index: _SymbolIndex,
    ) -> set[str]:
        try:
            tree = ast.parse(symbol.source_code)
        except SyntaxError:
            return set()

        collector = DependencyCollector()
        collector.visit(tree)

        resolved: set[str] = set()
        for raw_call in collector.dependencies:
            qualified = index.resolve(
                raw_call,
                file_path=symbol.file_path,
                class_name=symbol.class_name,
            )
            if (
                qualified is not None
                and qualified != symbol.qualified_name
                and qualified in index._by_qualified
            ):
                resolved.add(qualified)

        return resolved
