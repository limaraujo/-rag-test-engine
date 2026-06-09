from dataclasses import dataclass
import ast
from pathlib import Path
import sys
from typing import Iterator

from ingest.ast_utils import get_ast_from_file
from ingest.call_graph import CallGraph, CallGraphBuilder
from ingest.dependency_graph import DependencyGraph, DependencyGraphBuilder
from ingest.extract import SymbolExtractor
from ingest.models.ExtractedSymbol import ExtractedSymbol
from ingest.scanner import RepositoryScanner


@dataclass(frozen=True)
class ParsedFile:
	path: str
	tree: ast.AST


def parse_repository(root: str) -> Iterator[ParsedFile]:
	scanner = RepositoryScanner(root)
	for path in scanner.scan_repository():
		tree = get_ast_from_file(str(path))
		yield ParsedFile(path=str(path), tree=tree)


def parse_repository_symbols(root: str) -> Iterator[ExtractedSymbol]:
	"""Parse files and yield extracted symbols."""
	for parsed in parse_repository(root):
		source_code = Path(parsed.path).read_text(encoding="utf-8")
		extractor = SymbolExtractor(
			file_path=parsed.path,
			tree=parsed.tree,
			source_code=source_code
		)
		yield from extractor.extract()


def parse_file_symbols(path: str) -> Iterator[ExtractedSymbol]:
	"""Parse one Python file and yield extracted symbols."""
	file_path = Path(path)
	tree = get_ast_from_file(str(file_path))
	source_code = file_path.read_text(encoding="utf-8")
	extractor = SymbolExtractor(
		file_path=str(file_path),
		tree=tree,
		source_code=source_code
	)
	yield from extractor.extract()


def build_call_graph(
	symbols: list[ExtractedSymbol],
	root: str,
) -> CallGraph:
	"""Build a function/method call graph from extracted symbols."""
	return CallGraphBuilder(root).build(symbols)


def build_dependency_graph(root: str) -> DependencyGraph:
	"""Build a module/class dependency graph from Python files."""
	return DependencyGraphBuilder(root).build()


def parse_repository_graphs(
	root: str,
) -> tuple[list[ExtractedSymbol], CallGraph, DependencyGraph]:
	"""Extract symbols and build call and dependency graphs for a repository."""
	symbols = list(parse_repository_symbols(root))
	call_graph = build_call_graph(symbols, root)
	dependency_graph = build_dependency_graph(root)
	return symbols, call_graph, dependency_graph


if __name__ == "__main__":
	root = sys.argv[1] if len(sys.argv) > 1 else "."
	for parsed in parse_repository(root):
		print(parsed.path)
