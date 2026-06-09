import json
from pathlib import Path
import pytest
import mockes.exemplo as exemplo
from mockes.exemplo import main

class FakeSymbol:
    def __init__(self, file_path: str, data: dict):
        self.file_path = file_path
        self._data = data
        self.dump_called = 0

    def model_dump(self):
        self.dump_called += 1
        return self._data

def test_main_writes_json_and_prints_for_matching_symbol(tmp_path, monkeypatch, capsys):
    "Writes JSON with one symbol when a symbol's file_path matches the module file and prints the saved count."
    # Arrange: set module ROOT to a temporary directory
    exemplo.ROOT = tmp_path

    # target_path inside the module (the file being inspected by main)
    target_path = Path(exemplo.__file__).resolve()

    # Prepare symbols: one matches target_path, one does not
    matching = FakeSymbol(str(target_path), {"name": "matched_symbol", "value": 42})
    non_matching = FakeSymbol(str(Path("/some/other/file.py")), {"name": "other_symbol"})
    symbols = [non_matching, matching]

    # Stub parse_repository_symbols to ensure it's called with the expected root string
    def fake_parse_repository_symbols(root_str):
        assert root_str == str(tmp_path)
        return symbols
    monkeypatch.setattr(exemplo, "parse_repository_symbols", fake_parse_repository_symbols)

    # Capture the write_text call by patching Path.write_text (filesystem external)
    recorded = {}
    def fake_write_text(self, text, encoding="utf-8"):
        recorded['text'] = text
        recorded['encoding'] = encoding
        recorded['path'] = self
        return len(text)
    monkeypatch.setattr(Path, "write_text", fake_write_text)

    # Act
    main()

    # Assert: JSON written contains only the matching symbol's model_dump output
    expected = json.dumps([matching.model_dump() if False else {"name": "matched_symbol", "value": 42}], indent=2, ensure_ascii=False)
    # Build expected using the actual matching data to avoid duplication mistakes
    expected = json.dumps([{"name": "matched_symbol", "value": 42}], indent=2, ensure_ascii=False)
    assert recorded['text'] == expected
    assert recorded['encoding'] == "utf-8"
    assert recorded['path'] == tmp_path / "saida.json"

    # Assert: printed message includes the correct count and output path
    captured = capsys.readouterr()
    assert f"Saved 1 symbols to {tmp_path / 'saida.json'}" in captured.out

def test_main_writes_empty_list_when_no_symbols_match(tmp_path, monkeypatch, capsys):
    "Writes an empty JSON array and prints zero when no symbol file_path matches the module file."
    # Arrange
    exemplo.ROOT = tmp_path
    target_path = Path(exemplo.__file__).resolve()

    # All symbols point elsewhere
    symbols = [
        FakeSymbol(str(Path("/unrelated/file1.py")), {"id": 1}),
        FakeSymbol(str(Path("/unrelated/file2.py")), {"id": 2}),
    ]

    def fake_parse_repository_symbols(root_str):
        assert root_str == str(tmp_path)
        return symbols
    monkeypatch.setattr(exemplo, "parse_repository_symbols", fake_parse_repository_symbols)

    recorded = {}
    def fake_write_text(self, text, encoding="utf-8"):
        recorded['text'] = text
        recorded['encoding'] = encoding
        recorded['path'] = self
        return len(text)
    monkeypatch.setattr(Path, "write_text", fake_write_text)

    # Act
    main()

    # Assert: wrote an empty list JSON
    expected = json.dumps([], indent=2, ensure_ascii=False)
    assert recorded['text'] == expected
    assert recorded['encoding'] == "utf-8"
    assert recorded['path'] == tmp_path / "saida.json"

    # Assert printed message shows zero saved symbols
    captured = capsys.readouterr()
    assert f"Saved 0 symbols to {tmp_path / 'saida.json'}" in captured.out