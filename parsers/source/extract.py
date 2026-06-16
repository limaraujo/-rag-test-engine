import ast

from parsers.source.collectors.branches import BranchCollector
from parsers.source.collectors.dependency_collector import DependencyCollector
from parsers.source.collectors.exceptions import ExceptionCollector
from parsers.source.collectors.imports import ImportCollector
from parsers.source.heuristics.edge_cases import EdgeCaseInferer
from parsers.source.models.ExtractedSymbol import ExtractedSymbol
from parsers.source.text_utils import read_source_text

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
        self.source_code = source_code or read_source_text(file_path)
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

        edge_cases = sorted(
            set(edge_inferer.edge_cases) | set(self._class_init_hints(class_name))
        )

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
            edge_cases=edge_cases
        )

    def _class_init_hints(self, class_name: str | None) -> list[str]:
        if not class_name:
            return []

        class_node = self._find_class_node(class_name)
        if class_node is None or not self._is_dataclass(class_node):
            return []

        fields = self._dataclass_fields(class_node)
        if not fields:
            return [
                f"Classe @dataclass — instancie {class_name}(...) antes de chamar métodos."
            ]
        joined = ", ".join(fields)
        return [
            f"Classe @dataclass — instancie {class_name}({joined}=...) antes de chamar métodos."
        ]

    def _find_class_node(self, class_name: str) -> ast.ClassDef | None:
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return node
        return None

    @staticmethod
    def _is_dataclass(class_node: ast.ClassDef) -> bool:
        for decorator in class_node.decorator_list:
            label = ast.unparse(decorator)
            if label == "dataclass" or label.endswith(".dataclass"):
                return True
        return False

    @staticmethod
    def _dataclass_fields(class_node: ast.ClassDef) -> list[str]:
        fields: list[str] = []
        for item in class_node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                fields.append(item.target.id)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        fields.append(target.id)
        return fields

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
    