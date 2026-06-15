import pytest
from datetime import datetime, timezone
from types import SimpleNamespace
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# verifica TypeError quando o payload não é dict
def test_encode_type_error_when_payload_not_dict():
    jwt = object.__new__(PyJWT)
    jwt._jws = SimpleNamespace(encode=lambda *args, **kwargs: "TOKEN")
    with pytest.raises(TypeError) as exc:
        PyJWT.encode(jwt, payload="not a dict", key="secret")
    assert "Expecting a dict object" in str(exc.value)

# verifica exceção quando iss não é string
def test_encode_issuer_must_be_string_raises():
    jwt = object.__new__(PyJWT)
    jwt._encode_payload = lambda pl, headers=None, json_encoder=None: "encoded"
    jwt._jws = SimpleNamespace(encode=lambda *args, **kwargs: "TOKEN")
    with pytest.raises(TypeError) as exc:
        PyJWT.encode(jwt, {'iss': 123}, key="secret", algorithm=None)
    assert "Issuer (iss) must be a string." in str(exc.value)

# verifica happy path: converte claims datetime e passa payload transformado para _encode_payload
def test_encode_converts_datetime_claims_and_calls_encode_payload():
    jwt = object.__new__(PyJWT)
    captured = {}
    def fake_encode_payload(pl, headers=None, json_encoder=None):
        captured['pl'] = pl
        return "encoded-payload"
    jwt._encode_payload = fake_encode_payload
    jwt._jws = SimpleNamespace(encode=lambda json_payload, key, algorithm, headers, json_encoder, sort_headers: "TOKEN")
    payload = {'iss': 'issuer', 'exp': datetime(1970, 1, 1, 0, 0, 10, tzinfo=timezone.utc)}
    token = PyJWT.encode(jwt, payload, key='secret', algorithm='HS256', headers=None, json_encoder=None, sort_headers=True)
    assert token == "TOKEN"
    assert captured['pl']['exp'] == 10
    assert captured['pl']['iss'] == 'issuer'

# verifica que encode passa os argumentos esperados para _jws.encode
def test_encode_passes_arguments_to_jws():
    jwt = object.__new__(PyJWT)
    def fake_encode_payload(pl, headers=None, json_encoder=None):
        return "payload-json"
    jwt._encode_payload = fake_encode_payload
    captured = {}
    def fake_jws_encode(json_payload, key, algorithm, headers, json_encoder, sort_headers):
        captured['args'] = (json_payload, key, algorithm, headers, json_encoder, sort_headers)
        return "TOKEN"
    jwt._jws = SimpleNamespace(encode=fake_jws_encode)
    payload = {'iss': 'issuer'}
    token = PyJWT.encode(jwt, payload, key='mykey', algorithm='HS256', headers={'kid': 'k1'}, json_encoder=None, sort_headers=False)
    assert token == "TOKEN"
    assert captured['args'][0] == "payload-json"
    assert captured['args'][1] == 'mykey'
    assert captured['args'][2] == 'HS256'
    assert captured['args'][3] == {'kid': 'k1'}
    assert captured['args'][4] is None
    assert captured['args'][5] is False
