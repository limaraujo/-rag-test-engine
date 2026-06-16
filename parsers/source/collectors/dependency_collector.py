import ast
import builtins

BUILTINS = set(dir(builtins))


class DependencyCollector(ast.NodeVisitor):
    """Collect dependencies from call expressions."""

    def __init__(self) -> None:
        self.dependencies: set[str] = set()

    def visit_Call(self, node: ast.Call) -> None:
        dependency = self.extract_dependency(node.func)
        if dependency and not self._is_builtin(dependency):
            self.dependencies.add(dependency)

        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            if keyword.value is not None:
                self.visit(keyword.value)

    def extract_dependency(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):
            parent = self.extract_dependency(node.value)
            if parent:
                return f"{parent}.{node.attr}"
            return node.attr

        if isinstance(node, ast.Call):
            return self.extract_dependency(node.func)

        if isinstance(node, ast.Subscript):
            return self.extract_dependency(node.value)

        return None

    @staticmethod
    def _is_builtin(dependency: str) -> bool:
        root = dependency.split(".", 1)[0]
        return root in BUILTINS