import ast
from pathlib import Path

from ingest.collectors.branches import BranchCollector
from ingest.collectors.dependency_collector import DependencyCollector
from ingest.collectors.exceptions import ExceptionCollector
from ingest.collectors.imports import ImportCollector
from ingest.heuristics.edge_cases import EdgeCaseInferer
from ingest.models.ExtractedSymbol import ExtractedSymbol


class SymbolExtractor(ast.NodeVisitor):
    """Extract semantic symbols from a Python module."""

    def __init__(
        self,
        file_path: str,
        tree: ast.AST,
        source_code: str | None = None
    ) -> None:
        self.file_path = file_path
        self.tree = tree
        self.source_code = source_code or Path(file_path).read_text(encoding="utf-8")
        self.symbols: list[ExtractedSymbol] = []
        self.current_class: str | None = None
        self._function_depth = 0
        self._imports: list[str] = []

    def extract(self) -> list[ExtractedSymbol]:
        self._imports = self._collect_imports()
        self.visit(self.tree)
        return self.symbols

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if self._function_depth > 0:
            return

        self.symbols.append(
            self._build_symbol(
                node=node,
                symbol_type="class",
                class_name=None
            )
        )

        previous_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = previous_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._handle_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._handle_function(node)

    def _handle_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> None:
        is_top_level = self._function_depth == 0
        self._function_depth += 1
        try:
            if is_top_level:
                symbol_type = "method" if self.current_class else "function"
                self.symbols.append(
                    self._build_symbol(
                        node=node,
                        symbol_type=symbol_type,
                        class_name=self.current_class
                    )
                )
            self.generic_visit(node)
        finally:
            self._function_depth -= 1

    def _collect_imports(self) -> list[str]:
        collector = ImportCollector()
        collector.visit(self.tree)
        return sorted(collector.imports)

    def _build_symbol(
        self,
        node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
        symbol_type: str,
        class_name: str | None
    ) -> ExtractedSymbol:
        dep_collector = DependencyCollector()
        dep_collector.visit(node)

        exc_collector = ExceptionCollector()
        exc_collector.visit(node)

        branch_collector = BranchCollector()
        branch_collector.visit(node)

        edge_inferer = EdgeCaseInferer()
        edge_inferer.visit(node)

        return ExtractedSymbol(
            symbol_type=symbol_type,
            name=node.name,
            qualified_name=self._qualified_name(node.name, class_name),
            class_name=class_name,
            file_path=self.file_path,
            source_code=self._source_segment(node),
            imports=self._imports,
            dependencies=sorted(dep_collector.dependencies),
            exceptions=sorted(exc_collector.exceptions),
            decorators=self._decorators(node),
            docstring=ast.get_docstring(node),
            branches=branch_collector.branches,
            edge_cases=sorted(edge_inferer.edge_cases)
        )

    @staticmethod
    def _qualified_name(name: str, class_name: str | None) -> str:
        if class_name:
            return f"{class_name}.{name}"
        return name

    def _source_segment(self, node: ast.AST) -> str:
        segment = ast.get_source_segment(self.source_code, node)
        if segment:
            return segment
        return ast.unparse(node)

    def _decorators(
        self,
        node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
    ) -> list[str]:
        decorator_list = node.decorator_list
        decorators: list[str] = []
        for decorator in decorator_list:
            segment = ast.get_source_segment(self.source_code, decorator)
            decorators.append(segment if segment else ast.unparse(decorator))
        return decorators
    