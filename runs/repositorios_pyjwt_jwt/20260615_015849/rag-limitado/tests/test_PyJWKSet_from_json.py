import json
import pytest
from unittest.mock import patch
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

# happy path: Valid JSON string leads to from_dict called with parsed object
def test_from_json_happy_path_calls_from_dict_with_parsed_json():
    json_str = '{"keys": [1, 2, 3]}'
    expected_obj = {"keys": [1, 2, 3]}
    with patch('repositorios.pyjwt.jwt.api_jwk.PyJWKSet.from_dict', return_value='sentinel') as mock_from_dict:
        result = PyJWKSet.from_json(json_str)
        mock_from_dict.assert_called_once_with(expected_obj)
        assert result == 'sentinel'

# error path: invalid JSON raises JSONDecodeError
def test_from_json_invalid_json_raises_jsondecodeerror():
    invalid_json = '{"keys": [1, 2, 3}'  # missing closing brace
    with pytest.raises(json.JSONDecodeError):
        PyJWKSet.from_json(invalid_json)
