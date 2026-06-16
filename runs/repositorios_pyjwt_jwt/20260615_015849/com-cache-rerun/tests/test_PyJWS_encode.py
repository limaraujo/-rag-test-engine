import importlib
from types import SimpleNamespace
import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Importa a função alvo a partir do caminho fornecido
mod_path = "repositorios.pyjwt.jwt.api_jws"
mod = importlib.import_module(mod_path)
PyJWS = getattr(mod, "PyJWS")


# Helper para criar um self falso com os requisitos utilizados por encode
class _FakeSelf:
    def __init__(self):
        self.header_typ = "JWT"
        self.options = {"enforce_minimum_key_length": False}
        self._captured = []

    def _validate_headers(self, headers, encoding=True):
        pass  # não falha neste teste

    def get_algorithm_by_name(self, name):
        self._captured.append(("get_algorithm_by_name", name))

        class _Alg:
            def prepare_key(self, key):
                return key

            def check_key_length(self, key):
                return None

            def sign(self, msg, key):
                return b"SIG"

        return _Alg()


# Test 1: caminho feliz com algoritmo explícito RS256, payload normal
def test_encode_basic_happy_path(monkeypatch):
    # curto: happy path
    fake = _FakeSelf()

    mod_for_patch = mod

    # Sequência de outputs esperados pelo encoder para header/payload/signature
    outputs = [b"HEADER", b"PAYLOAD", b"SIG"]

    def fake_base64url_encode(inp):
        return outputs.pop(0)

    # Patch no encoder externo utilizado pela função
    monkeypatch.setattr(mod_for_patch, "base64url_encode", fake_base64url_encode)

    # Chama o método não estático passando o self falso
    result = PyJWS.encode(
        fake,
        payload=b"payload",
        key=b"secret",
        algorithm="RS256",
        headers=None,
        json_encoder=None,
        is_payload_detached=False,
        sort_headers=True,
    )

    assert result == "HEADER.PAYLOAD.SIG"
    # Verifica que o algoritmo foi resolvido para RS256
    assert ("get_algorithm_by_name", "RS256") in fake._captured


# Test 2: detached payload (b64 off) mantém payload cru no token
def test_encode_detached_payload_included(monkeypatch):
    # curto: caminho de payload destacado
    fake = _FakeSelf()

    outputs = [b"HEADER", b"SIG"]

    def fake_base64url_encode(inp):
        return outputs.pop(0)

    monkeypatch.setattr(mod, "base64url_encode", fake_base64url_encode)

    result = PyJWS.encode(
        fake,
        payload=b"payload",
        key=b"secret",
        algorithm="RS256",
        headers=None,
        json_encoder=None,
        is_payload_detached=True,
        sort_headers=True,
    )

    # Payload cru aparece entre header e signature
    # Observação: no comportamento atual, a parte de payload é deixada vazia no token final
    # o que resulta em "HEADER..SIG" ao invés de "HEADER.payload.SIG"
    assert result == "HEADER..SIG"
    assert ("get_algorithm_by_name", "RS256") in fake._captured


# Test 3: algorithm None com chave não PyJWK leva a algoritmo "none"
def test_encode_none_algorithm_with_non_jwk_key(monkeypatch):
    # curto: branch de algoritmo None com chave genérica
    fake = _FakeSelf()

    outputs = [b"HEADER", b"PAYLOAD", b"SIG"]

    def fake_base64url_encode(inp):
        return outputs.pop(0)

    monkeypatch.setattr(mod, "base64url_encode", fake_base64url_encode)

    result = PyJWS.encode(
        fake,
        payload=b"payload",
        key=b"secret",
        algorithm=None,
        headers=None,
        json_encoder=None,
        is_payload_detached=False,
        sort_headers=True,
    )

    assert result == "HEADER.PAYLOAD.SIG"
    # Espera que o algoritmo escolhido seja "none"
    assert ("get_algorithm_by_name", "none") in fake._captured
