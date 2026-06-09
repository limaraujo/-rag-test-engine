import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ingest.parser import parse_file_symbols, parse_repository_symbols
from retrieval.embeddings import embed_symbols


def main() -> None:
    root = ROOT
    target_path: Path | None = None

    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1]).resolve()

    if target_path:
        symbols = parse_file_symbols(str(target_path))
    else:
        symbols = parse_repository_symbols(str(root))
    records = embed_symbols(symbols)

    output_path = root / "embedding_records.json"
    output_path.write_text(
        json.dumps(records, indent=2, ensure_ascii=True),
        encoding="utf-8"
    )
    print(f"Saved {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
