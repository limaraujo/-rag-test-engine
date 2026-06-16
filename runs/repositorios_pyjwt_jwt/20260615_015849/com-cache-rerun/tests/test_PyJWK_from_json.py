import json
import pytest
from unittest.mock import patch
from repositorios.pyjwt.jwt.api_jwk import PyJWK


# Verifica: JSON é parseado e PyJWK.from_dict é chamado com o dict resultante e algoritmo fornecido (happy path)
def test_from_json_parses_json_and_calls_from_dict_with_algorithm():
    data = '{"kid":"1","kty":"oct"}'
    parsed = {'kid': '1', 'kty': 'oct'}
    with patch('repositorios.pyjwt.jwt.api_jwk.json.loads', return_value=parsed) as mock_json_loads:
        with patch('repositorios.pyjwt.jwt.api_jwk.PyJWK.from_dict', return_value='sentinel') as mock_from_dict:
            result = PyJWK.from_json(data, algorithm='RS256')
            assert result == 'sentinel'
            mock_json_loads.assert_called_once_with(data)
            mock_from_dict.assert_called_once_with(parsed, 'RS256')

# Verifica: algoritmo=None é repassado para PyJWK.from_dict (branch quando não especificado)
def test_from_json_none_algorithm_passed_through():
    data = '{"kid":"2","kty":"oct"}'
    parsed = {'kid': '2', 'kty': 'oct'}
    with patch('repositorios.pyjwt.jwt.api_jwk.json.loads', return_value=parsed) as mock_json_loads:
        with patch('repositorios.pyjwt.jwt.api_jwk.PyJWK.from_dict', return_value='sentinel_none') as mock_from_dict:
            result = PyJWK.from_json(data, algorithm=None)
            assert result == 'sentinel_none'
            mock_json_loads.assert_called_once_with(data)
            mock_from_dict.assert_called_once_with(parsed, None)

# Verifica: exceção de JSON é propagada quando o JSON é inválido
def test_from_json_invalid_json_raises_json_decode_error():
    with patch('repositorios.pyjwt.jwt.api_jwk.json.loads', side_effect=json.JSONDecodeError("Expecting value", "not-json", 0)):
        with pytest.raises(json.JSONDecodeError):
            PyJWK.from_json('not-json')
