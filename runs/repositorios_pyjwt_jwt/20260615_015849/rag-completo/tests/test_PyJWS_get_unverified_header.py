import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# curto: happy path - retorna os headers sem modificações e validação passa
def test_get_unverified_header_happy_path():
    headers = {'alg': 'HS256', 'typ': 'JWT', 'kid': 'abc'}
    instance = PyJWS.__new__(PyJWS)

    captured = {}

    def fake_load(jwt):
        captured['jwt'] = jwt
        return (None, None, headers)

    def fake_validate(hdrs):
        captured['validated_headers'] = hdrs

    instance._load = fake_load
    instance._validate_headers = fake_validate

    result = instance.get_unverified_header('my_jwt_string')

    assert result is headers
    assert captured['jwt'] == 'my_jwt_string'
    assert captured['validated_headers'] is headers

# curto: exceção de validação é propagada
def test_get_unverified_header_raises_from_validate():
    headers = {'typ': 'JWT'}
    instance = PyJWS.__new__(PyJWS)

    def fake_load(jwt):
        return (None, None, headers)

    def fake_validate(hdrs):
        raise ValueError("invalid headers")

    instance._load = fake_load
    instance._validate_headers = fake_validate

    with pytest.raises(ValueError):
        instance.get_unverified_header('jwt123')

# curto: _load recebe o jwt passado pelo caller
def test_get_unverified_header_passes_jwt_to_load():
    headers = {'foo': 'bar'}
    instance = PyJWS.__new__(PyJWS)

    def fake_load(jwt):
        assert jwt == 'jwt-for-test'
        return (None, None, headers)

    def fake_validate(hdrs):
        pass

    instance._load = fake_load
    instance._validate_headers = fake_validate

    result = instance.get_unverified_header('jwt-for-test')
    assert result is headers
