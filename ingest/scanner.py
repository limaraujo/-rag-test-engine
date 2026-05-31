from pathlib import Path

class RepositoryScanner:
    
    IGNORE_EXTENSIONS = {'.md', '.txt', '.json', '.yaml', '.yml', '.csv'}
    IGNORE_DIRS = {'.git', '.pytest_cache', '.venv', '__pycache__', 'venv', 'env'}
    
    def __init__(self, root: str):
        self.root = Path(root)

    def scan_repository(self):
        for path in self.root.rglob('*.py'):
            
            if self._ignored(path):
                continue
            
            yield path
            
    def _ignored(self, path: Path):
        return (
            path.suffix in self.IGNORE_EXTENSIONS
            or any(part in self.IGNORE_DIRS for part in path.parts)
        )
