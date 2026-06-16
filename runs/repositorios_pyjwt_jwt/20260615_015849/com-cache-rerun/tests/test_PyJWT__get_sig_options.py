import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# Verifica _get_sig_options com várias combinações de verify_signature e enforce_minimum_key_length (inclui default quando ausente)
@pytest.mark.parametrize("options, expected", [
    ({"verify_signature": True, "enforce_minimum_key_length": True},
     {"verify_signature": True, "enforce_minimum_key_length": True}),
    ({"verify_signature": False, "enforce_minimum_key_length": False},
     {"verify_signature": False, "enforce_minimum_key_length": False}),
    ({"verify_signature": True},
     {"verify_signature": True, "enforce_minimum_key_length": False}),
    ({"verify_signature": False},
     {"verify_signature": False, "enforce_minimum_key_length": False}),
])
def test__get_sig_options_various(options, expected):
    obj = PyJWT.__new__(PyJWT)
    obj.options = options
    assert obj._get_sig_options() == expected
