import pytest
from unittest.mock import Mock
from repositorios.pyjwt.jwt.api_jws import PyJWS

# curto
# happy path: retorna o cabeçalho não verificado e validação ocorre com sucesso
def test_get_unverified_header_happy_path():
    jws = PyJWS()
    header = {"alg": "HS256", "typ": "JWT"}
    jws._load = Mock(return_value=[None, None, header])
    jws._validate_headers = Mock()
    result = jws.get_unverified_header(b"dummy.jwt")
    assert result == header
    jws._validate_headers.assert_called_with(header)

# curto
# exceção propagada: _validate_headers levanta uma exceção, que deve ser propagada
def test_get_unverified_header_propagates_exception():
    jws = PyJWS()
    header = {"alg": "none"}
    jws._load = Mock(return_value=[None, None, header])
    jws._validate_headers = Mock(side_effect=ValueError("bad headers"))
    with pytest.raises(ValueError, match="bad headers"):
        jws.get_unverified_header("jwt")

# curto
# checagem de passagem do jwt para _load: a função deve encaminhar o token corretamente
def test_get_unverified_header_passes_jwt_to_load():
    jws = PyJWS()
    seen = {}
    def fake_load(jwt):
        seen['jwt'] = jwt
        return [None, None, {"header": 1}]
    jws._load = fake_load
    jws._validate_headers = Mock()
    jws.get_unverified_header("token123")
    assert seen['jwt'] == "token123"
