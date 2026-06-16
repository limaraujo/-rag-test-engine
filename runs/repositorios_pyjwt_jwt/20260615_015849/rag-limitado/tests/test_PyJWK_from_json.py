import json
import pytest
from unittest.mock import patch
from repositorios.pyjwt.jwt.api_jwk import PyJWK

# happy path: verifica que, com algoritmo fornecido, PyJWK.from_dict é chamado com o dict parseado e o algoritmo
def test_from_json_happy_path_with_algorithm():
    sentinel = object()
    with patch('repositorios.pyjwt.jwt.api_jwk.PyJWK.from_dict', return_value=sentinel) as mock_from_dict:
        result = PyJWK.from_json('{"k":"v"}', algorithm='RS256')
        mock_from_dict.assert_called_once_with({"k": "v"}, 'RS256')
        assert result is sentinel

# happy path: verifica que, ao não fornecer algoritmo, None é passado para from_dict
def test_from_json_happy_path_without_algorithm():
    sentinel = object()
    with patch('repositorios.pyjwt.jwt.api_jwk.PyJWK.from_dict', return_value=sentinel) as mock_from_dict:
        result = PyJWK.from_json('{"a":1}')
        mock_from_dict.assert_called_once_with({"a": 1}, None)
        assert result is sentinel

# verifica que json.loads é usado e o resultado é repassado para from_dict
def test_from_json_uses_json_loads_and_passes_parsed_object():
    sentinel = object()
    with patch('repositorios.pyjwt.jwt.api_jwk.json.loads', return_value={'patched': 'yes'}) as mock_load:
        with patch('repositorios.pyjwt.jwt.api_jwk.PyJWK.from_dict', return_value=sentinel) as mock_from_dict:
            result = PyJWK.from_json('ignored', algorithm='ALG')
            mock_load.assert_called_once_with('ignored')
            mock_from_dict.assert_called_once_with({'patched': 'yes'}, 'ALG')
            assert result is sentinel

# exceção: JSON inválido deve propagar JSONDecodeError
def test_from_json_invalid_json_raises_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        PyJWK.from_json('not json', None)
