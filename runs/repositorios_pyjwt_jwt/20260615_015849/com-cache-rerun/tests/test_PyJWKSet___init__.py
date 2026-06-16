import pytest
from unittest.mock import patch
from repositorios.pyjwt.jwt.exceptions import PyJWTError, MissingCryptographyError, PyJWKSetError
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

import pytest
from unittest.mock import patch

from repositorios.pyjwt.jwt.exceptions import PyJWTError, MissingCryptographyError, PyJWKSetError
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

# test 1: invalid inputs (empty collection and non-list)
@pytest.mark.parametrize("keys,expected_message", [
    ([], "The JWK Set did not contain any keys"),
    ("notalist", "Invalid JWK Set value"),
])
def test_init_invalid_inputs(keys, expected_message):
    with pytest.raises(PyJWKSetError) as exc:
        PyJWKSet(keys)
    assert str(exc.value) == expected_message

# test 2: happy path with usable keys
def test_init_happy_path():
    keys = [{"kid": "1"}, {"kid": "2"}]

    with patch("repositorios.pyjwt.jwt.api_jwk.PyJWK", side_effect=lambda k: f"JWK-{k['kid']}"):
        jwk_set = PyJWKSet(keys)
        assert jwk_set.keys == ["JWK-1", "JWK-2"]

# test 3: all keys unusable (non-missing-cryptography), should raise final PyJWKSetError
def test_init_no_usable_keys_raises():
    keys = [{"kid": "a"}, {"kid": "b"}]

    def mock_jwk(key):
        raise PyJWTError("unusable key")

    with patch("repositorios.pyjwt.jwt.api_jwk.PyJWK", side_effect=mock_jwk):
        with pytest.raises(PyJWKSetError) as exc:
            PyJWKSet(keys)
        assert str(exc.value) == "The JWK Set did not contain any usable keys. Perhaps 'cryptography' is not installed?"

# test 4: missing cryptography should propagate
def test_init_propagates_missing_cryptography_error():
    keys = [{"kid": "a"}]

    with patch("repositorios.pyjwt.jwt.api_jwk.PyJWK", side_effect=MissingCryptographyError("missing cryptography")):
        with pytest.raises(MissingCryptographyError):
            PyJWKSet(keys)
