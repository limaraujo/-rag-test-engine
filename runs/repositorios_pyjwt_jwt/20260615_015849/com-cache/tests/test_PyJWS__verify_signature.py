import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidAlgorithmError, InvalidSignatureError
from repositorios.pyjwt.jwt.api_jws import PyJWS
import types
import types

import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidAlgorithmError, InvalidSignatureError
from repositorios.pyjwt.jwt.api_jws import PyJWS

# verifica erro quando o header não contém o algoritmo
def test_verify_signature_missing_alg_raises():
    jws = PyJWS.__new__(PyJWS)
    jws.options = {}
    header = {}
    with pytest.raises(InvalidAlgorithmError) as exc:
        jws._verify_signature(b"sign", header, b"sig", key=b"key")
    assert "Algorithm not specified" in str(exc.value)

# verifica erro quando o algoritmo está fora da lista permitida
def test_verify_signature_invalid_alg_not_allowed():
    jws = PyJWS.__new__(PyJWS)
    jws.options = {}
    header = {"alg": "HS256"}
    with pytest.raises(InvalidAlgorithmError) as exc:
        jws._verify_signature(b"sign", header, b"sig", key=b"key", algorithms=["RS256"])
    assert "The specified alg value is not allowed" in str(exc.value)

# verifica erro quando o algoritmo não é suportado pela implementação
def test_verify_signature_algorithm_not_supported_raises_InvalidAlgorithmError():
    jws = PyJWS.__new__(PyJWS)
    jws.options = {}

    header = {"alg": "HS256"}
    def _get_alg(self, name):
        raise NotImplementedError
    import types
    jws.get_algorithm_by_name = types.MethodType(_get_alg, jws)

    with pytest.raises(InvalidAlgorithmError) as exc:
        jws._verify_signature(b"sign", header, b"sig", key=b"key")
    assert "Algorithm not supported" in str(exc.value)

# verifica falha de assinatura gera InvalidSignatureError
def test_verify_signature_failure_raises_InvalidSignatureError():
    jws = PyJWS.__new__(PyJWS)
    jws.options = {"enforce_minimum_key_length": False}
    header = {"alg": "HS256"}

    class _FakeAlg:
        def prepare_key(self, key):
            return key
        def check_key_length(self, key):
            return None
        def verify(self, signing_input, key, signature):
            return False

    def _get_alg(self, name):
        return _FakeAlg()

    import types
    jws.get_algorithm_by_name = types.MethodType(_get_alg, jws)

    with pytest.raises(InvalidSignatureError):
        jws._verify_signature(b"sign", header, b"sig", key=b"key")
