import json
import pytest
import repositorios.code_katas.src.forbes as ForbesModule
from repositorios.code_katas.src.forbes import get_json

# happy path: lê e retorna JSON de arquivo existente definido por FPATH
def test_get_json_happy_path(monkeypatch, tmp_path):
    data = {"city": "Example", "lat_lon": [0, 0]}
    p = tmp_path / "data.json"
    p.write_text(json.dumps(data))
    monkeypatch.setattr(ForbesModule, "FPATH", str(p))
    assert get_json() == data

# exceção FileNotFoundError: arquivo inexistente apontado por FPATH
def test_get_json_file_not_found(monkeypatch, tmp_path):
    missing = tmp_path / "no_such_file.json"
    monkeypatch.setattr(ForbesModule, "FPATH", str(missing))
    with pytest.raises(FileNotFoundError):
        get_json()

# exceção JSONDecodeError: conteúdo não é JSON válido
def test_get_json_invalid_json(monkeypatch, tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json")
    monkeypatch.setattr(ForbesModule, "FPATH", str(bad))
    with pytest.raises(json.JSONDecodeError):
        get_json()
