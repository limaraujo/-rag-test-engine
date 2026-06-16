import json
from pathlib import Path
import pytest
import mockes.exemplo as exemplo
from mockes.exemplo import main


class SimpleSymbol:
    def __init__(self, file_path: str, data: dict):
        self.file_path = file_path
        self._data = data

    def model_dump(self):
        return self._data


def test_main_writes_json_and_prints_for_matching_symbol(tmp_path, monkeypatch, capsys):
    """Writes JSON with one symbol when a symbol's file_path matches the module file and prints the saved count."""
    # Arrange: set module ROOT to a temporary directory
    monkeypatch.setattr(exemplo, "ROOT", tmp_path)

    # target_path inside the module (the file being inspected by main)
    target_path = Path(exemplo.__file__).resolve()

    # Prepare symbols: one matches target_path, one does not
    matching = SimpleSymbol(str(target_path), {"name": "matched_symbol", "value": 42})
    non_matching = SimpleSymbol(str(Path("/some/other/file.py")), {"name": "other_symbol"})
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
    expected = json.dumps([{"name": "matched_symbol", "value": 42}], indent=2, ensure_ascii=False)
    assert recorded["text"] == expected
    assert recorded["encoding"] == "utf-8"
    assert recorded["path"] == tmp_path / "saida.json"

    # Assert: printed message includes the correct count and output path
    captured = capsys.readouterr()
    assert f"Saved 1 symbols to {tmp_path / 'saida.json'}" in captured.out


def test_main_writes_empty_list_when_no_symbols_match(tmp_path, monkeypatch, capsys):
    """Writes an empty JSON array and prints zero when no symbol file_path matches the module file."""
    # Arrange
    monkeypatch.setattr(exemplo, "ROOT", tmp_path)
    target_path = Path(exemplo.__file__).resolve()

    symbols = [
        SimpleSymbol(str(Path("/unrelated/file1.py")), {"id": 1}),
        SimpleSymbol(str(Path("/unrelated/file2.py")), {"id": 2}),
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


def test_main_writes_json_for_multiple_matching_symbols(tmp_path, monkeypatch, capsys):
    """Writes JSON with multiple matching symbols when several file_paths match the module file and prints the count."""
    # Arrange
    monkeypatch.setattr(exemplo, "ROOT", tmp_path)
    target_path = Path(exemplo.__file__).resolve()

    data1 = {"name": "first", "value": 1}
    data2 = {"name": "second", "value": 2}
    symbols = [
        SimpleSymbol(str(target_path), data1),
        SimpleSymbol(str(target_path), data2),
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

    # Assert: JSON contains both dumped symbols in order
    expected = json.dumps([data1, data2], indent=2, ensure_ascii=False)
    assert recorded["text"] == expected
    assert recorded["encoding"] == "utf-8"
    assert recorded["path"] == tmp_path / "saida.json"

    # Assert printed message shows two saved symbols
    captured = capsys.readouterr()
    assert f"Saved 2 symbols to {tmp_path / 'saida.json'}" in captured.out
