from pathlib import Path
import ast

def get_ast_from_file(file_path: str):
    files = list(Path(file_path).rglob('*.py'))
    if not files:
        raise FileNotFoundError(f"No Python files found in {file_path}")

