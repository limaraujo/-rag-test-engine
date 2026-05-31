from ingest.models.ExtractedSymbol import ExtractedSymbol


def to_embedding_doc(
    symbol: ExtractedSymbol,
) -> tuple[str, dict]:
    """Build embedding text and metadata from an extracted symbol."""
    def format_list(values: list[str]) -> str:
        return ", ".join(values) if values else "<none>"

    lines: list[str] = [
        f"symbol: {symbol.qualified_name}",
        f"type: {symbol.symbol_type}",
        f"file: {symbol.file_path}",
        f"class: {symbol.class_name or '<none>'}",
    ]

    if symbol.docstring is not None:
        lines.append(f"docstring: {symbol.docstring}")

    lines.append(f"decorators: {format_list(symbol.decorators)}")
    lines.append(f"imports: {format_list(symbol.imports)}")
    lines.append(f"dependencies: {format_list(symbol.dependencies)}")
    lines.append(f"exceptions: {format_list(symbol.exceptions)}")
    lines.append(f"branches: {symbol.branches}")
    lines.append(f"edge_cases: {format_list(symbol.edge_cases)}")

    lines.append("code:")
    lines.append(symbol.source_code)

    text = "\n".join(lines)
    metadata = {
        "qualified_name": symbol.qualified_name,
        "symbol_type": symbol.symbol_type,
        "class_name": symbol.class_name,
        "file_path": symbol.file_path,
    }

    return text, metadata
    



