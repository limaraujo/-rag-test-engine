import io
import pytest
from unittest.mock import patch
from repositorios.code_katas.src.forbes import get_json

# happy path: retorna dados quando json.load funciona
def test_get_json_happy_path_opens_correct_file_and_returns_data():
    path_info = {}
    def fake_open(path, mode):
        path_info['path'] = path
        path_info['mode'] = mode
        return io.StringIO('{"a": 1}')
    def fake_json_load(fileobj):
        path_info['fileobj'] = fileobj
        return {'a': 1}
    with patch('repositorios.code_katas.src.forbes.open', side_effect=fake_open) as _open:
        with patch('repositorios.code_katas.src.forbes.json.load', side_effect=fake_json_load) as _json_load:
            data = get_json()
            assert data == {'a': 1}
            assert path_info['path'] is not None
            assert path_info['mode'] == 'r'
            assert isinstance(path_info['fileobj'], io.StringIO)

# exceção listada: json.load levanta ValueError, deve ser propagado
def test_get_json_raises_when_json_load_fails():
    with patch('repositorios.code_katas.src.forbes.open', return_value=io.StringIO('{}')):
        with patch('repositorios.code_katas.src.forbes.json.load', side_effect=ValueError("bad json")):
            with pytest.raises(ValueError):
                get_json()

# borda/exceção: open levanta FileNotFoundError, deve ser propagado
def test_get_json_propagates_file_not_found():
    with patch('repositorios.code_katas.src.forbes.open', side_effect=FileNotFoundError("no such file")):
        with pytest.raises(FileNotFoundError):
            get_json()
