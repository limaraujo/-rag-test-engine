import ast
from pathlib import Path

from parsers.source.text_utils import read_source_text


def get_ast_from_file(file_path: str) -> ast.AST:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    source = read_source_text(path)
    return ast.parse(source, filename=str(path))

