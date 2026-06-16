import json
import pytest
from repositorios.code_katas.src.forbes import get_json
import repositorios.code_katas.src.forbes as forbes
import repositorios.code_katas.src.forbes as forbes

import json
import pytest
from repositorios.code_katas.src.forbes import get_json

# curto: happy path - lê JSON válido de FPATH configurado e retorna o dict
def test_get_json_happy_path(tmp_path):
    import repositorios.code_katas.src.forbes as forbes
    data = {"name": "Alice", "age": 30}
    fpath = tmp_path / "data.json"
    fpath.write_text(json.dumps(data))
    forbes.FPATH = str(fpath)
    assert forbes.get_json() == data

# curto: exceção JSON malformado - JSONDecodeError é propagada
def test_get_json_invalid_json_raises(tmp_path):
    import repositorios.code_katas.src.forbes as forbes
    fpath = tmp_path / "bad.json"
    fpath.write_text("{ invalid json: }")
    forbes.FPATH = str(fpath)
    with pytest.raises(json.JSONDecodeError):
        forbes.get_json()
