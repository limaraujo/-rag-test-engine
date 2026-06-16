import pytest
from datetime import datetime
from calendar import timegm
from repositorios.pyjwt.jwt.api_jwt import PyJWT
import types

import pytest
from datetime import datetime
from calendar import timegm
from repositorios.pyjwt.jwt.api_jwt import PyJWT



# Verifica TypeError quando payload não é dict (caso de borda)
def test_encode_raises_typeerror_on_non_dict_payload():
    jwt = PyJWT.__new__(PyJWT)
    with pytest.raises(TypeError):
        jwt.encode(payload=123, key="secret")


# Verifica TypeError quando iss não é string
def test_encode_raises_typeerror_when_iss_not_string():
    jwt = PyJWT.__new__(PyJWT)
    with pytest.raises(TypeError):
        jwt.encode(payload={"iss": 42}, key="secret")


# Verifica conversão de time claims e chamada de encode (caminho feliz)
def test_encode_converts_time_claims_and_calls_jws_encode():
    jwt = PyJWT.__new__(PyJWT)

    class MockJWS:
        def __init__(self):
            self.calls = []
        def encode(self, json_payload, key, algorithm, headers, json_encoder, sort_headers=True):
            self.calls.append({
                "json_payload": json_payload,
                "key": key,
                "algorithm": algorithm,
                "headers": headers,
                "json_encoder": json_encoder,
                "sort_headers": sort_headers,
            })
            return "MOCK_TOKEN"

    mock_jws = MockJWS()
    jwt._jws = mock_jws

    captured = {}

    def fake_encode_payload(self, payload, headers=None, json_encoder=None):
        captured['payload'] = payload.copy()
        captured['headers'] = headers
        captured['json_encoder'] = json_encoder
        return "ENCODED_PAYLOAD"

    import types
    jwt._encode_payload = types.MethodType(fake_encode_payload, jwt)

    dt = datetime(2020, 1, 2, 3, 4, 5)

    result = jwt.encode(payload={"iss": "issuer", "exp": dt}, key="secret", algorithm="HS256")

    assert result == "MOCK_TOKEN"
    assert 'payload' in captured
    assert captured['payload']['exp'] == timegm(dt.utctimetuple())
    assert captured['payload']['iss'] == "issuer"

    assert len(mock_jws.calls) == 1
    call = mock_jws.calls[0]
    assert call['json_payload'] == "ENCODED_PAYLOAD"
    assert call['key'] == "secret"
    assert call['algorithm'] == "HS256"
    assert call['headers'] is None
    assert call['sort_headers'] is True
