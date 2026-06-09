from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from config.settings import settings


def setup_logging(log_file: Path | None = None) -> Path:
    """Configura logging no terminal e em arquivo."""
    if log_file is None:
        log_dir = Path(settings.LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"pipeline_{timestamp}.log"
    else:
        log_file.parent.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    root.handlers.clear()

    file_fmt = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_fmt = logging.Formatter("%(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(file_fmt)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_fmt)

    root.addHandler(file_handler)
    root.addHandler(console_handler)

    return log_file
