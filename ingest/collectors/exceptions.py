import ast

class ExceptionCollector(ast.NodeVisitor):

    def __init__(self):
        self.exceptions: set[str] = set()

    def visit_Raise(self, node: ast.Raise):

        self.exceptions.update(
            self.extract_exception(node.exc)
        )

        self.generic_visit(node)

    def visit_ExceptHandler(
        self,
        node: ast.ExceptHandler
    ):

        self.exceptions.update(
            self.extract_exception(node.type)
        )

        self.generic_visit(node)

    def extract_exception(
        self,
        node: ast.AST | None
    ) -> list[str]:

        if node is None:
            return []

        if isinstance(node, ast.Name):
            return [node.id]

        if isinstance(node, ast.Call):
            return self.extract_exception(node.func)

        if isinstance(node, ast.Attribute):
            parent = self.extract_exception(node.value)

            return [
                f"{p}.{node.attr}"
                for p in parent
            ] or [node.attr]

        if isinstance(node, ast.Tuple):
            exceptions = []

            for elt in node.elts:
                exceptions.extend(
                    self.extract_exception(elt)
                )

            return exceptions

        return []