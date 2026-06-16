from __future__ import annotations

from pathlib import Path

UTF8_BOM = "\ufeff"


def strip_utf8_bom(text: str) -> str:
    """Remove BOM UTF-8 no início do texto (comum em respostas LLM e arquivos Windows)."""
    if text.startswith(UTF8_BOM):
        return text[1:]
    return text


def read_source_text(path: Path | str) -> str:
    """
    Lê código-fonte Python tolerando BOM.

    Usa ``utf-8-sig`` para descartar BOM ao ler arquivos do disco.
    """
    return Path(path).read_text(encoding="utf-8-sig")
