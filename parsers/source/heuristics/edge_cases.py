import ast

from parsers.source.collectors.exceptions import ExceptionCollector


class EdgeCaseInferer(ast.NodeVisitor):
	"""Infer simple edge cases from a symbol AST."""

	def __init__(self) -> None:
		self.edge_cases: set[str] = set()
		self._exception_helper = ExceptionCollector()
		self._has_division = False
		self._has_subscript = False
		self._saw_zero_division = False
		self._saw_index_error = False

	def visit_BinOp(self, node: ast.BinOp) -> None:
		if isinstance(node.op, (ast.Div, ast.FloorDiv)):
			self._has_division = True
			if self._is_zero_constant(node.right) or self._saw_zero_division:
				self.edge_cases.add("division_by_zero")
		self.generic_visit(node)

	def visit_Subscript(self, node: ast.Subscript) -> None:
		self._has_subscript = True
		if self._saw_index_error:
			self.edge_cases.add("index_out_of_bounds")
		self.generic_visit(node)

	def visit_Compare(self, node: ast.Compare) -> None:
		if self._is_len_empty_check(node):
			self.edge_cases.add("empty_collection")
		self.generic_visit(node)

	def visit_Raise(self, node: ast.Raise) -> None:
		self._check_exception(node.exc)
		self.generic_visit(node)

	def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
		self._check_exception(node.type)
		self.generic_visit(node)

	def _check_exception(self, node: ast.AST | None) -> None:
		names = self._exception_helper.extract_exception(node)
		if self._has_exception(names, "ValueError"):
			self.edge_cases.add("invalid_input")
		if self._has_exception(names, "KeyError"):
			self.edge_cases.add("missing_key")
		if self._has_exception(names, "ZeroDivisionError"):
			self._saw_zero_division = True
			if self._has_division:
				self.edge_cases.add("division_by_zero")
		if self._has_exception(names, "IndexError"):
			self._saw_index_error = True
			if self._has_subscript:
				self.edge_cases.add("index_out_of_bounds")

	@staticmethod
	def _has_exception(names: list[str], target: str) -> bool:
		for name in names:
			if name == target or name.endswith(f".{target}"):
				return True
		return False

	@staticmethod
	def _is_zero_constant(node: ast.AST) -> bool:
		if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, complex)):
			return node.value == 0
		if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
			return EdgeCaseInferer._is_zero_constant(node.operand)
		return False

	@staticmethod
	def _is_len_call(node: ast.AST) -> bool:
		return (
			isinstance(node, ast.Call)
			and isinstance(node.func, ast.Name)
			and node.func.id == "len"
			and len(node.args) == 1
		)

	@staticmethod
	def _is_zero(node: ast.AST) -> bool:
		return isinstance(node, ast.Constant) and node.value == 0

	@staticmethod
	def _is_one(node: ast.AST) -> bool:
		return isinstance(node, ast.Constant) and node.value == 1

	def _is_len_empty_check(self, node: ast.Compare) -> bool:
		left = node.left
		for op, comparator in zip(node.ops, node.comparators):
			if self._is_empty_len_pair(left, op, comparator):
				return True
			if self._is_empty_len_pair(comparator, op, left):
				return True
			left = comparator
		return False

	def _is_empty_len_pair(
		self,
		left: ast.AST,
		op: ast.cmpop,
		right: ast.AST
	) -> bool:
		if not self._is_len_call(left):
			return False
		if self._is_zero(right):
			return isinstance(op, (ast.Eq, ast.LtE))
		if self._is_one(right):
			return isinstance(op, ast.Lt)
		return False
