import json
import pytest
import repositorios.code_katas.src.forbes as ForbesModule
from repositorios.code_katas.src.forbes import get_json

# curto: testando caminho feliz com dois conjuntos de dados válidos
@pytest.mark.parametrize("idx, data", [
    (0, {"country": "France", "city": "Paris"}),
    (1, {"city": "Tokyo", "lat_lon": {"lat": 35.6895, "lon": 139.6917}}),
])
def test_get_json_happy_path(tmp_path, idx, data):
    f = tmp_path / f"data_{idx}.json"
    f.write_text(json.dumps(data))
    ForbesModule.FPATH = str(f)
    assert get_json() == data

# curto: exceção FileNotFoundError quando o arquivo não existe
def test_get_json_file_not_found(tmp_path):
    missing = tmp_path / "missing.json"
    ForbesModule.FPATH = str(missing)
    with pytest.raises(FileNotFoundError):
        get_json()

# curto: JSON inválido gera json.JSONDecodeError
def test_get_json_invalid_json(tmp_path):
    f = tmp_path / "bad.json"
    f.write_text("not json")
    ForbesModule.FPATH = str(f)
    with pytest.raises(json.JSONDecodeError):
        get_json()
