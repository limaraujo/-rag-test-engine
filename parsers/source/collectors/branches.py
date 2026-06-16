import ast


class BranchCollector(ast.NodeVisitor):
	"""Count branching constructs; each If/Elif is counted as one branch."""

	def __init__(self) -> None:
		self.branches = 0

	def visit_If(self, node: ast.If) -> None:
		self.branches += 1
		self.generic_visit(node)

	def visit_For(self, node: ast.For) -> None:
		self.branches += 1
		self.generic_visit(node)

	def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
		self.branches += 1
		self.generic_visit(node)

	def visit_While(self, node: ast.While) -> None:
		self.branches += 1
		self.generic_visit(node)

	def visit_Try(self, node: ast.Try) -> None:
		self.branches += 1
		self.generic_visit(node)

	def visit_Match(self, node: ast.Match) -> None:
		self.branches += 1
		self.generic_visit(node)
