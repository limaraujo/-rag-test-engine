import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS
from repositorios.pyjwt.jwt.exceptions import DecodeError

import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

try:
    from repositorios.pyjwt.jwt.exceptions import DecodeError
except Exception:
    class DecodeError(Exception):
        pass


# Helper subclass to mock internal behavior of PyJWS without real crypto
class DummyPyJWS(PyJWS):
    def __init__(self, payload: bytes, header: dict, signing_input: bytes, signature: bytes):
        self.options = {"verify_signature": True}
        self._payload = payload
        self._header = header
        self._signing_input = signing_input
        self._signature = signature

    def _load(self, jwt):
        return self._payload, self._signing_input, self._header, self._signature

    def _validate_headers(self, header):
        return None

    def _verify_signature(self, signing_input, header, signature, key, algorithms, options=None):
        return None


# Verifica caminho feliz: kwargs são aceitos, warning emitida, e retorno está correto
def test_decode_complete_happy_path_with_kwargs():
    # header sem b64 false; payload simples; assinatura simulada
    payload = b"PAYLOAD"
    header = {"alg": "HS256"}
    signing_input = b"header.payload.signature"
    signature = b"sig"

    obj = DummyPyJWS(payload, header, signing_input, signature)

    with pytest.warns(Warning):
        result = obj.decode_complete(
            jwt="token",
            key="secret",
            algorithms=["HS256"],
            foo="bar"  # extra kwarg; should emit deprecation warning
        )

    assert result["payload"] == payload
    assert result["header"] == header
    assert result["signature"] == signature


# Verifica DecodeError quando verificação de assinatura está ativada sem algoritmos fornecidos
def test_decode_complete_requires_algorithms_when_verifying_signature():
    payload = b"PAYLOAD"
    header = {"alg": "HS256"}
    signing_input = b"header.payload.signature"
    signature = b"sig"

    obj = DummyPyJWS(payload, header, signing_input, signature)

    with pytest.raises(DecodeError):
        obj.decode_complete(jwt="token", key="secret", algorithms=None)


# Verifica branch b64=False com detached_payload fornecido
def test_decode_complete_b64_false_with_detached_payload():
    payload = b"payload"
    header = {"b64": False, "crit": ["b64"]}
    signing_input = b"header.payload.signature"
    signature = b"sig"
    detached = b"DETACHED"

    obj = DummyPyJWS(payload, header, signing_input, signature)

    result = obj.decode_complete(
        jwt="token",
        key="secret",
        algorithms=["HS256"],
        detached_payload=detached
    )

    assert result["payload"] == detached
    assert result["header"] == header
    assert result["signature"] == signature


# Verifica DecodeError quando b64=False, mas detached_payload não fornecido
def test_decode_complete_b64_false_missing_detached_payload_raises():
    payload = b"payload"
    header = {"b64": False, "crit": ["b64"]}
    signing_input = b"header.payload.signature"
    signature = b"sig"

    obj = DummyPyJWS(payload, header, signing_input, signature)

    with pytest.raises(DecodeError):
        obj.decode_complete(jwt="token", key="secret", algorithms=["HS256"])
