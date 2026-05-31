from pathlib import Path
import ast


def get_ast_from_file(file_path: str) -> ast.AST:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    source = path.read_text(encoding="utf-8")
    return ast.parse(source, filename=str(path))

