import json
import pytest
from unittest.mock import patch
from repositorios.pyjwt.jwt.api_jwk import PyJWK
from repositorios.pyjwt.jwt.exceptions import PyJWKError

import json
import pytest
from unittest.mock import patch
from repositorios.pyjwt.jwt.api_jwk import PyJWK


# Try to import PyJWKError for an explicit exception propagation test; skip if unavailable
try:
    from repositorios.pyjwt.jwt.exceptions import PyJWKError
except Exception:
    PyJWKError = None


# short: happy path with explicit algorithm
@pytest.mark.parametrize("algorithm", ["RS256", None])
def test_from_json_happy_path_calls_from_dict_with_parsed_json(algorithm):
    data = '{"k": "v"}'
    captured = []

    def side_effect(*args, **kwargs):
        # Support both classmethod and staticmethod binding styles
        if len(args) == 3:
            obj, alg = args[1], args[2]
        elif len(args) == 2:
            obj, alg = args[0], args[1]
        else:
            obj, alg = None, None
        captured.append((obj, alg))
        return "SENTINEL"

    with patch('repositorios.pyjwt.jwt.api_jwk.PyJWK.from_dict', side_effect=side_effect) as _:
        result = PyJWK.from_json(data, algorithm)

    assert result == "SENTINEL"
    assert captured == [({"k": "v"}, algorithm)]


# short: invalid JSON should raise JSONDecodeError
def test_from_json_invalid_json_raises_json_decode_error():
    data = '{"k": "v"'  # missing closing brace -> invalid JSON
    with pytest.raises(json.JSONDecodeError):
        PyJWK.from_json(data)


# short: propagation of exception raised by from_dict
def test_from_json_propagates_exception_from_from_dict():
    if PyJWKError is None:
        pytest.skip("PyJWKError not available in this environment")

    with patch('repositorios.pyjwt.jwt.api_jwk.PyJWK.from_dict', side_effect=PyJWKError("boom")):
        with pytest.raises(PyJWKError):
            PyJWK.from_json('{"a": 1}', None)
