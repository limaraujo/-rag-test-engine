import importlib
import types
import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# PyJWS.encode tests for a single symbol: ensure encoding path works with mocked crypto and header handling

def _setup_env(monkeypatch):
    api_jws = importlib.import_module("repositorios.pyjwt.jwt.api_jws")
    PyJWS = api_jws.PyJWS

    class _FakeAlg:
        def prepare_key(self, key):
            return key

        def check_key_length(self, key):
            return None

        def sign(self, msg, key):
            return b"signature"

    inst = PyJWS.__new__(PyJWS)
    inst.header_typ = "JWT"
    inst.options = {"enforce_minimum_key_length": False}
    inst._validate_headers = lambda headers, encoding=True: None
    inst.get_algorithm_by_name = lambda name: _FakeAlg()

    captured_header = {}

    def _fake_json_dumps(header, separators, cls, sort_keys):
        captured_header.clear()
        captured_header.update(header.copy())
        return '{"dummy":1}'

    monkeypatch.setattr(api_jws, "base64url_encode", lambda b: b"b64")
    monkeypatch.setattr(api_jws, "json", types.SimpleNamespace(dumps=_fake_json_dumps))

    return api_jws, inst, captured_header

# 1) Verifica caminho feliz com chave de string e algorithm=None
def test_encode_happy_path_string_key_none_algorithm(monkeypatch):
    # short: happy path where algorithm is determined from string key and no headers override
    api_jws, inst, captured_header = _setup_env(monkeypatch)

    result = api_jws.PyJWS.encode(inst, payload=b"payload", key="secret", algorithm=None, headers=None, json_encoder=None, is_payload_detached=False, sort_headers=True)

    # Algoritmo esperado: none (porque key não é PyJWK)
    assert captured_header.get("alg") == "none"
    assert result == "b64.b64.b64"

# 2) Verifica override de alg via headers
def test_encode_header_alg_override(monkeypatch):
    api_jws, inst, captured_header = _setup_env(monkeypatch)

    headers = {"alg": "RS256"}
    result = api_jws.PyJWS.encode(inst, payload=b"payload", key="secret", algorithm=None, headers=headers, json_encoder=None, is_payload_detached=False, sort_headers=True)

    # Header deve refletir o valor de headers["alg"]
    assert captured_header.get("alg") == "RS256"
    assert result == "b64.b64.b64"

# 3) Verifica detach via header b64=False e inclusão de 'crit' com 'b64'
def test_encode_detached_payload_header_crit(monkeypatch):
    api_jws, inst, captured_header = _setup_env(monkeypatch)

    headers = {"alg": "HS256", "b64": False}
    result = api_jws.PyJWS.encode(inst, payload=b"payload", key="secret", algorithm=None, headers=headers, json_encoder=None, is_payload_detached=False, sort_headers=True)

    # Quando b64 é usado via header e chega como False, should set header["b64"]=False e adicionar "crit": ["b64"]
    assert captured_header.get("b64") is False
    assert captured_header.get("crit") == ["b64"]
    # O token deve refletir payload detach (segundo segmento vazio)
    assert result == "b64..b64"
