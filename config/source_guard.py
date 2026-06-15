from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from config.settings import ROOT, settings
from parsers.source.path_filters import ScanResult, scan_python_files

logger = logging.getLogger(__name__)


class SourceDirBlockedError(RuntimeError):
    """Execução bloqueada por validação estrita de ``source_dir``."""


@dataclass(frozen=True)
class SourceDirValidation:
    warnings: tuple[str, ...]
    blocked: bool
    block_reason: str | None = None


def validate_source_dir(
    source_dir: str | Path,
    *,
    allow_risky: bool = False,
    strict: bool | None = None,
    scan_result: ScanResult | None = None,
) -> SourceDirValidation:
    """
    Valida ``source_dir`` antes da ingestão.

    Em modo não estrito (padrão), emite avisos e continua.
    Em modo estrito, bloqueia execuções arriscadas salvo ``allow_risky``.
    """
    src = Path(source_dir).resolve()
    strict_mode = settings.SOURCE_DIR_STRICT if strict is None else strict
    threshold = settings.SOURCE_DIR_PY_WARN_THRESHOLD
    allow = allow_risky or settings.SOURCE_DIR_ALLOW_RISKY

    result = scan_result if scan_result is not None else scan_python_files(src)
    warnings: list[str] = []

    if src == ROOT.resolve():
        msg = (
            f"source_dir é a raiz do RAG test engine ({src}); "
            "aponte para o código do projeto alvo"
        )
        warnings.append(msg)
        logger.warning("[security] %s", msg)

    if result.included > threshold:
        msg = (
            f"source_dir contém {result.included} arquivos Python incluídos "
            f"(limite de aviso: {threshold}); verifique o diretório alvo"
        )
        warnings.append(msg)
        logger.warning("[security] %s", msg)

    if strict_mode and warnings and not allow:
        reason = warnings[0]
        logger.error("[security] execução bloqueada (SOURCE_DIR_STRICT): %s", reason)
        return SourceDirValidation(
            warnings=tuple(warnings),
            blocked=True,
            block_reason=reason,
        )

    return SourceDirValidation(warnings=tuple(warnings), blocked=False)


def ensure_source_dir_allowed(
    source_dir: str | Path,
    *,
    allow_risky: bool = False,
    strict: bool | None = None,
    scan_result: ScanResult | None = None,
) -> SourceDirValidation:
    """Valida e levanta ``SourceDirBlockedError`` quando bloqueado."""
    validation = validate_source_dir(
        source_dir,
        allow_risky=allow_risky,
        strict=strict,
        scan_result=scan_result,
    )
    if validation.blocked:
        raise SourceDirBlockedError(validation.block_reason or "source_dir bloqueado")
    return validation
