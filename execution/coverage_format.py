from __future__ import annotations

import re


def parse_missing_ranges(text: str) -> list[int]:
    """
    Expande linhas faltantes (formato pytest-cov term-missing) em inteiros ordenados.

    Exemplos::

        "8, 12-14, 22"  →  [8, 12, 13, 14, 22]
        "30-32"         →  [30, 31, 32]
    """
    lines: list[int] = []
    for part in re.split(r"[,\s]+", text.strip()):
        if not part:
            continue
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                lines.extend(range(int(start), int(end) + 1))
            except ValueError:
                pass
        else:
            digits = re.sub(r"[^\d]", "", part)
            if digits:
                lines.append(int(digits))
    return sorted(set(lines))


def format_ranges(line_numbers: list[int]) -> str:
    """
    Comprime inteiros ordenados em intervalos compactos.

    Exemplo: [8, 12, 13, 14, 22] → "8, 12-14, 22"
    """
    if not line_numbers:
        return ""
    sorted_lines = sorted(set(line_numbers))
    parts: list[str] = []
    start = end = sorted_lines[0]

    for number in sorted_lines[1:]:
        if number == end + 1:
            end = number
        else:
            parts.append(str(start) if start == end else f"{start}-{end}")
            start = end = number
    parts.append(str(start) if start == end else f"{start}-{end}")
    return ", ".join(parts)
