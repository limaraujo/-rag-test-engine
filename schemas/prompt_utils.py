from __future__ import annotations


def compact_rag_snippet(text: str, *, max_chars: int, label: str = "") -> str:
    """
    Reduz trechos RAG para o prompt: extrai só o código quando possível e trunca.
    """
    stripped = text.strip()
    if "code:\n" in stripped:
        stripped = stripped.split("code:\n", 1)[1].strip()
    if label and not stripped.startswith(label):
        stripped = f"{label}\n{stripped}"

    if len(stripped) <= max_chars:
        return stripped

    return stripped[:max_chars] + "\n… (truncado)"
