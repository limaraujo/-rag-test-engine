import json
import pytest
import repositorios.code_katas.src.forbes as Forbes
from repositorios.code_katas.src.forbes import get_json

# happy path: lê JSON válido de um arquivo temporário
def test_get_json_happy_path(tmp_path):
    data = {"hello": "world", "numbers": [1, 2, 3]}
    f = tmp_path / "data.json"
    f.write_text(json.dumps(data))
    Forbes.FPATH = str(f)
    assert Forbes.get_json() == data

# exception: arquivo não encontrado deve levantar FileNotFoundError
def test_get_json_file_not_found():
    Forbes.FPATH = "non_existent_file_12345.json"
    with pytest.raises(FileNotFoundError):
        Forbes.get_json()

# exception: JSON inválido deve levantar JSONDecodeError
def test_get_json_invalid_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{invalid: json")
    Forbes.FPATH = str(p)
    with pytest.raises(json.JSONDecodeError):
        Forbes.get_json()
