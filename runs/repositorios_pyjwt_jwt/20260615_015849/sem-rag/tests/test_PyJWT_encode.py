import pytest
from datetime import datetime, timezone
from types import MethodType
from repositorios.pyjwt.jwt.api_jwt import PyJWT



# Verifica TypeError quando payload não é dict (caso de borda)
def test_encode_raises_type_error_for_non_dict_payload():
    jwt = PyJWT()
    with pytest.raises(TypeError):
        jwt.encode(payload=42, key="dummy-key")


# Verifica TypeError para issuer (iss) não sendo string (caso de borda)
def test_encode_raises_type_error_for_issuer_non_string():
    jwt = PyJWT()
    with pytest.raises(TypeError) as exc:
        jwt.encode(payload={"iss": 123}, key="dummy-key")
    assert "Issuer (iss) must be a string." in str(exc.value)


# Verifica conversão de time claims datetime para int e envio para encode_jws (caminho feliz com claims de tempo)
def test_encode_time_claims_are_converted_and_forwarded():
    jwt = PyJWT()

    # Dummy JWS para capturar chamadas
    class DummyJWS:
        def __init__(self):
            self.calls = None

        def encode(self, json_payload, key, algorithm, headers, json_encoder, sort_headers=True):
            self.calls = {
                "json_payload": json_payload,
                "key": key,
                "algorithm": algorithm,
                "headers": headers,
                "json_encoder": json_encoder,
                "sort_headers": sort_headers,
            }
            return "dummy_jws_return"

    jwt._jws = DummyJWS()

    captured = {}

    def fake_encode_payload(self, p, headers=None, json_encoder=None):
        captured["payload"] = p
        captured["headers"] = headers
        captured["json_encoder"] = json_encoder
        return "encoded_payload_string"

    jwt._encode_payload = MethodType(fake_encode_payload, jwt)

    payload = {
        "iss": "issuer",
        "exp": datetime(1970, 1, 1, tzinfo=timezone.utc),
        "iat": datetime(1970, 1, 1, tzinfo=timezone.utc),
        "nbf": datetime(1970, 1, 1, tzinfo=timezone.utc),
        "sub": "subject",
    }

    result = jwt.encode(payload=payload, key="dummy-key")

    assert result == "dummy_jws_return"
    assert isinstance(captured["payload"]["exp"], int)
    assert captured["payload"]["exp"] == 0
    assert captured["payload"]["iat"] == 0
    assert captured["payload"]["nbf"] == 0


# Verifica passagem correta de headers e json_encoder para o encoder externo e retorno do valor (caminho feliz)
def test_encode_forwards_headers_and_json_encoder_and_returns_value():
    jwt = PyJWT()

    # Dummy JWS para capturar chamadas
    class DummyJWS:
        def __init__(self):
            self.calls = None

        def encode(self, json_payload, key, algorithm, headers, json_encoder, sort_headers=True):
            self.calls = {
                "json_payload": json_payload,
                "key": key,
                "algorithm": algorithm,
                "headers": headers,
                "json_encoder": json_encoder,
                "sort_headers": sort_headers,
            }
            return "dummy_jws_output"

    jwt._jws = DummyJWS()

    captured = {}

    def fake_encode_payload(self, p, headers=None, json_encoder=None):
        captured["payload"] = p
        captured["headers"] = headers
        captured["json_encoder"] = json_encoder
        return "encoded_payload_blob"

    jwt._encode_payload = MethodType(fake_encode_payload, jwt)

    payload = {"iss": "issuer"}
    headers = {"kid": "abc"}
    json_encoder = "CUSTOM_ENCODER"

    result = jwt.encode(payload=payload, key="dummy-key", headers=headers, json_encoder=json_encoder)

    assert result == "dummy_jws_output"
    # Verifica que os headers e json_encoder são repassados para o encoder externo
    assert jwt._jws.calls["headers"] is headers
    assert jwt._jws.calls["json_encoder"] == json_encoder
    # Verifica que o payload passado ao _encode_payload corresponde ao input (cópia) sem mutação inesperada
    assert captured["payload"]["iss"] == "issuer"
