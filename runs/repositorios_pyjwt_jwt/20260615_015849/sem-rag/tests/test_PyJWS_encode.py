import importlib
import json
import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Import the target module and helpers
mod = importlib.import_module("repositorios.pyjwt.jwt.api_jws")
PyJWS = getattr(mod, "PyJWS")
_ALGORITHM_UNSET = getattr(mod, "_ALGORITHM_UNSET")
base64url_encode = getattr(mod, "base64url_encode")
base64url_decode = getattr(mod, "base64url_decode")
PyJWK = getattr(mod, "PyJWK")

# -------------- Test helpers --------------

class _FakeAlg:
    def __init__(self, name: str):
        self.name = name

    def check_key_length(self, key):
        return None

    def prepare_key(self, key):
        return key

    def sign(self, signing_input, key):
        return b"signature"

# -------------- Tests --------------

# Verifica caminho feliz: algoritmo padrão HS256 quando algoritmo não é especificado e chave simples
def test_encode_default_algorithm_with_plain_key():
    # Prepare a PyJWS instance mock
    inst = object.__new__(PyJWS)
    inst.header_typ = "JWT"
    inst.options = {"enforce_minimum_key_length": False}
    inst._validate_headers = lambda headers, encoding=True: None
    inst.get_algorithm_by_name = lambda name: _FakeAlg(name)

    payload = b"payload"
    key = "secret"

    # Execute
    encoded = inst.encode(payload, key, algorithm=_ALGORITHM_UNSET, headers=None, json_encoder=None, is_payload_detached=False, sort_headers=True)

    # Compute expected header and payload segments
    header_dict = {"typ": "JWT", "alg": "HS256"}
    header_json = json.dumps(header_dict, separators=(",", ":"), sort_keys=True).encode()
    header_b64 = base64url_encode(header_json)

    payload_b64 = base64url_encode(payload)

    expected = (header_b64 + b"." + payload_b64 + b"." + base64url_encode(b"signature")).decode("utf-8")
    assert encoded == expected

# Verifica comportamento quando key é PyJWK: o algoritmo deve usar key.algorithm_name
def test_encode_with_pyjwk_algorithm_from_key():
    mod_jwk = PyJWK  # alias for clarity

    class DummyPyJWK(mod_jwk):
        def __init__(self):
            # Avoid calling super().__init__ if it requires complex init
            self.algorithm_name = "RS256"
            self.key = "dummykey"

    dummy = DummyPyJWK()

    inst = object.__new__(PyJWS)
    inst.header_typ = "JWT"
    inst.options = {"enforce_minimum_key_length": False}
    inst._validate_headers = lambda headers, encoding=True: None
    inst.get_algorithm_by_name = lambda name: _FakeAlg(name)  # type: ignore[arg-type]

    payload = b"payload"

    encoded = inst.encode(payload, dummy, algorithm=None, headers=None, json_encoder=None, is_payload_detached=False, sort_headers=True)

    header_dict = {"typ": "JWT", "alg": "RS256"}
    header_json = json.dumps(header_dict, separators=(",", ":"), sort_keys=True).encode()
    header_b64 = base64url_encode(header_json)
    payload_b64 = base64url_encode(payload)

    expected = (header_b64 + b"." + payload_b64 + b"." + base64url_encode(b"signature")).decode("utf-8")
    assert encoded == expected

# Verifica detecção de detach quando headers b64=False: payload não codificado e header com "b64" e "crit"
def test_encode_detached_payload_with_b64_false_header():
    inst = object.__new__(PyJWS)
    inst.header_typ = "JWT"
    inst.options = {"enforce_minimum_key_length": False}
    inst._validate_headers = lambda headers, encoding=True: None
    inst.get_algorithm_by_name = lambda name: _FakeAlg(name)

    payload = b"payload"

    headers = {"b64": False}
    encoded = inst.encode(payload, "secret", algorithm=_ALGORITHM_UNSET, headers=headers, json_encoder=None, is_payload_detached=None, sort_headers=True)

    parts = encoded.split(".")
    assert len(parts) == 3  # header, empty payload, signature
    header_b64 = parts[0].encode("utf-8")
    header_json = base64url_decode(header_b64)
    header = json.loads(header_json)

    # Verifica que o header contenha b64 e a lista de crit
    assert header.get("b64") is False
    crit = header.get("crit")
    assert isinstance(crit, list) and "b64" in crit

    # Verificação adicional: payload "segregado" está vazio
    assert parts[1] == ""

# Verifica sobreposição de algoritmo via headers: se headers["alg"] sobrescreve algoritmo detectado
def test_encode_headers_override_algorithm():
    inst = object.__new__(PyJWS)
    inst.header_typ = "JWT"
    inst.options = {"enforce_minimum_key_length": False}
    inst._validate_headers = lambda headers, encoding=True: None
    inst.get_algorithm_by_name = lambda name: _FakeAlg(name)

    payload = b"payload"
    headers = {"alg": "RS512"}

    encoded = inst.encode(payload, "secret", algorithm=_ALGORITHM_UNSET, headers=headers, json_encoder=None, is_payload_detached=False, sort_headers=True)

    # Decode header para verificar alg definido via headers
    header_b64 = encoded.split(".")[0].encode("utf-8")
    header_json = base64url_decode(header_b64)
    header = json.loads(header_json)
    assert header.get("alg") == "RS512"
