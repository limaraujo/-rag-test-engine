import json
import pytest
from pathlib import Path
from repositorios.code_katas.src import forbes
from repositorios.code_katas.src.forbes import get_json

# Teste feliz: retorna o JSON lido de um arquivo válido definido por FPATH
def test_get_json_happy_path(monkeypatch, tmp_path):
    data = {"city": "Test", "lat_lon": [0, 0], "value": 42}
    fpath = tmp_path / "valid.json"
    fpath.write_text(json.dumps(data))
    monkeypatch.setattr(forbes, "FPATH", str(fpath))
    assert forbes.get_json() == data

# Teste de erro: arquivo não encontrado levanta FileNotFoundError
def test_get_json_file_not_found(monkeypatch, tmp_path):
    missing = tmp_path / "missing.json"
    monkeypatch.setattr(forbes, "FPATH", str(missing))
    with pytest.raises(FileNotFoundError):
        forbes.get_json()

# Teste de erro: conteúdo inválido levanta JSONDecodeError
def test_get_json_invalid_json(monkeypatch, tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json")
    monkeypatch.setattr(forbes, "FPATH", str(bad))
    with pytest.raises(json.JSONDecodeError):
        forbes.get_json()
