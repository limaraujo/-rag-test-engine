import ast


class ImportCollector(ast.NodeVisitor):

    def __init__(self):
        self.imports: set[str] = set()

    def visit_Import(
        self,
        node: ast.Import
    ):

        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(
        self,
        node: ast.ImportFrom
    ):

        module = node.module or ""

        for alias in node.names:

            if module:
                self.imports.add(
                    f"{module}.{alias.name}"
                )
            else:
                self.imports.add(alias.name)