from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from ingest.path_filters import ScanResult, scan_python_files


class RepositoryScanner:
    def __init__(self, root: str) -> None:
        self.root = Path(root)

    def scan_repository(self) -> Iterator[Path]:
        result = scan_python_files(self.root)
        self._last_scan = result
        yield from result.files

    @property
    def last_scan(self) -> ScanResult | None:
        return getattr(self, "_last_scan", None)
