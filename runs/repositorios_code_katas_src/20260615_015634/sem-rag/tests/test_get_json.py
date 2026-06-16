import json
import pytest
import repositorios.code_katas.src.forbes as forbes_module
from repositorios.code_katas.src.forbes import get_json

# curto: happy path - JSON válido deve ser carregado corretamente
def test_get_json_happy_path(tmp_path, monkeypatch):
    data = {"key": "value"}
    fpath = tmp_path / "data.json"
    fpath.write_text(json.dumps(data))
    monkeypatch.setattr(forbes_module, "FPATH", str(fpath))
    assert get_json() == data

# curto: JSON inválido deve levantar JSONDecodeError
def test_get_json_invalid_json_raises(tmp_path, monkeypatch):
    fpath = tmp_path / "bad.json"
    fpath.write_text("not json")
    monkeypatch.setattr(forbes_module, "FPATH", str(fpath))
    with pytest.raises(json.JSONDecodeError):
        get_json()

# curto: caminho inexistente deve levantar FileNotFoundError
def test_get_json_file_not_found_raises(tmp_path, monkeypatch):
    missing_path = tmp_path / "missing.json"
    monkeypatch.setattr(forbes_module, "FPATH", str(missing_path))
    with pytest.raises(FileNotFoundError):
        get_json()
