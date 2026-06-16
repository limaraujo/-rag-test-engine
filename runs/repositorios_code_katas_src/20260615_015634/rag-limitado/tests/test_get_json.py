import importlib
import json
import pytest
from repositorios.code_katas.src.forbes import get_json

# happy path: lê JSON válido do arquivo apontado por FPATH
def test_get_json_happy_path(tmp_path, monkeypatch):
    mod = importlib.import_module("repositorios.code_katas.src.forbes")
    data = {"city": "New York", "value": 100}
    path = tmp_path / "data.json"
    path.write_text(json.dumps(data))
    monkeypatch.setattr(mod, "FPATH", str(path))
    assert mod.get_json() == data

# exception: arquivo não encontrado levanta FileNotFoundError
def test_get_json_file_not_found(monkeypatch):
    mod = importlib.import_module("repositorios.code_katas.src.forbes")
    missing_path = "/path/que/nao/existe.json"
    monkeypatch.setattr(mod, "FPATH", missing_path)
    with pytest.raises(FileNotFoundError):
        mod.get_json()

# exception: conteúdo do arquivo não é JSON válido levanta JSONDecodeError
def test_get_json_invalid_json(tmp_path, monkeypatch):
    mod = importlib.import_module("repositorios.code_katas.src.forbes")
    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{ bad json: }")
    monkeypatch.setattr(mod, "FPATH", str(bad_path))
    with pytest.raises(json.JSONDecodeError):
        mod.get_json()
