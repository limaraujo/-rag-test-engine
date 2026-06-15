import json
import pytest
import importlib
from repositorios.code_katas.src.forbes import get_json

# Verifica caminho feliz: lê JSON válido de arquivo apontado por FPATH e retorna os dados
def test_get_json_happy_path(tmp_path):
    module = importlib.import_module("repositorios.code_katas.src.forbes")
    data = {"city": "New York", "lat_lon": [40.7128, -74.0060]}
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps(data))
    module.FPATH = str(data_file)
    assert module.get_json() == data

# Verifica exceção FileNotFoundError quando o arquivo não existe
def test_get_json_raises_FileNotFound_error(tmp_path):
    module = importlib.import_module("repositorios.code_katas.src.forbes")
    missing_path = tmp_path / "nonexistent.json"
    module.FPATH = str(missing_path)
    with pytest.raises(FileNotFoundError):
        module.get_json()

# Verifica JSONDecodeError quando conteúdo é inválido
def test_get_json_invalid_json_raises_JSONDecodeError(tmp_path):
    module = importlib.import_module("repositorios.code_katas.src.forbes")
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{ bad json")
    module.FPATH = str(bad_file)
    with pytest.raises(json.JSONDecodeError):
        module.get_json()

# Verifica que json.load é chamado com um objeto arquivo e retorna o valor mockado
def test_get_json_calls_json_load_with_file_object(tmp_path, monkeypatch):
    module = importlib.import_module("repositorios.code_katas.src.forbes")
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps({"a": 1}))
    module.FPATH = str(data_file)

    captured = {}

    def fake_load(file_obj):
        captured['has_read'] = hasattr(file_obj, "read")
        captured['type'] = type(file_obj)
        return {"ok": True}

    monkeypatch.setattr(module.json, "load", fake_load, raising=True)

    result = module.get_json()
    assert result == {"ok": True}
    assert captured.get('has_read', False)
