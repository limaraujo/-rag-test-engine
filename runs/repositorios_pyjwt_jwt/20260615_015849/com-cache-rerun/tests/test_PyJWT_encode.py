import datetime
import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT


# Verifica TypeError quando payload não é dict
def test_encode_raises_type_error_if_payload_not_dict():
    inst = PyJWT.__new__(PyJWT)  # bypass __init__
    with pytest.raises(TypeError):
        inst.encode(payload=[1, 2], key="k", algorithm=None)

# Verifica conversão de time claims (exp) de datetime para int (time since epoch)
def test_encode_converts_datetime_time_claims_to_int():
    inst = PyJWT.__new__(PyJWT)

    captured_payload = {}

    def fake_encode_payload(payload, headers=None, json_encoder=None):
        captured_payload.update(payload)
        return {"encoded": "payload"}

    class DummyJWS:
        def encode(self, json_payload, key, algorithm, headers, json_encoder, sort_headers=True):
            return "signed_token"

    inst._encode_payload = fake_encode_payload
    inst._jws = DummyJWS()

    payload = {"exp": datetime.datetime(1970, 1, 1, 0, 0, 0)}
    result = inst.encode(payload=payload, key="k", algorithm=None, headers=None, json_encoder=None, sort_headers=True)

    assert result == "signed_token"
    assert "exp" in captured_payload
    assert captured_payload["exp"] == 0

# Verifica TypeError quando iss não é string
def test_encode_issuer_must_be_string_error():
    inst = PyJWT.__new__(PyJWT)
    with pytest.raises(TypeError):
        inst.encode(payload={"iss": 123}, key="k", algorithm=None)

# Verifica passagem do json_payload para o encode do PyJWT JWS
def test_encode_passes_json_payload_to_jws_encode():
    inst = PyJWT.__new__(PyJWT)

    captured = {}

    class DummyJWS:
        def encode(self, json_payload, key, algorithm, headers, json_encoder, sort_headers=True):
            captured["json_payload"] = json_payload
            captured["key"] = key
            captured["algorithm"] = algorithm
            captured["headers"] = headers
            captured["json_encoder"] = json_encoder
            captured["sort_headers"] = sort_headers
            return "signed_token"

    inst._jws = DummyJWS()
    inst._encode_payload = lambda payload, headers=None, json_encoder=None: {"encoded": "payload"}

    result = inst.encode(payload={"a": 1}, key="k", algorithm="HS256", headers={"kid": "1"}, json_encoder=None, sort_headers=False)

    assert result == "signed_token"
    assert captured["json_payload"] == {"encoded": "payload"}
