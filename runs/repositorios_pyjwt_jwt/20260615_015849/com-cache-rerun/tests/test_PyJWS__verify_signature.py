import pytest
from types import MethodType
from repositorios.pyjwt.jwt.exceptions import InvalidAlgorithmError, InvalidKeyError, InvalidSignatureError
from repositorios.pyjwt.jwt.api_jws import PyJWS

import pytest
from types import MethodType

from repositorios.pyjwt.jwt.exceptions import InvalidAlgorithmError, InvalidKeyError, InvalidSignatureError
from repositorios.pyjwt.jwt.api_jws import PyJWS


def _make_pyjws_with_alg(alg_name="RS256", enforce_minimum=False, alg_obj=None, not_implemented=False):
    pyjws = PyJWS.__new__(PyJWS)
    pyjws.options = {"enforce_minimum_key_length": enforce_minimum}
    if alg_obj is None:
        class DummyAlg:
            def check_key_length(self, key):
                return None
            def prepare_key(self, key):
                return key
            def verify(self, msg, key, sig):
                return True
        alg_obj = DummyAlg()
    def _get_algorithm_by_name(self_ref, name):
        if not_implemented:
            raise NotImplementedError
        if name != alg_name:
            raise NotImplementedError
        return alg_obj
    pyjws.get_algorithm_by_name = MethodType(_get_algorithm_by_name, pyjws)
    return pyjws


# Test 1: missing alg in header should raise InvalidAlgorithmError
def test_missing_alg_in_header_raises_InvalidAlgorithmError():
    pyjws = _make_pyjws_with_alg()
    signing_input = b"dummy_signing_input"
    header = {}  # missing "alg"
    signature = b"signature"
    with pytest.raises(InvalidAlgorithmError) as exc:
        pyjws._verify_signature(signing_input, header, signature, key=b"key")
    assert "Algorithm not specified" in str(exc.value)


# Test 2: alg not in allowed list should raise InvalidAlgorithmError
def test_alg_not_allowed_raises_InvalidAlgorithmError():
    pyjws = _make_pyjws_with_alg()
    signing_input = b"input"
    header = {"alg": "HS256"}
    signature = b"sig"
    with pytest.raises(InvalidAlgorithmError) as exc:
        pyjws._verify_signature(signing_input, header, signature, key=b"key", algorithms=["RS256"])
    assert "The specified alg value is not allowed" in str(exc.value)


# Test 3: NotImplementedError from algorithm lookup should map to InvalidAlgorithmError
def test_algorithm_not_implemented_raises_InvalidAlgorithmError():
    pyjws = _make_pyjws_with_alg(not_implemented=True)
    signing_input = b"input"
    header = {"alg": "RS256"}
    signature = b"sig"
    with pytest.raises(InvalidAlgorithmError) as exc:
        pyjws._verify_signature(signing_input, header, signature, key=b"key", algorithms=["RS256"])
    assert "Algorithm not supported" in str(exc.value)


# Test 4: minimum key length enforcement triggers InvalidKeyError when enabled
def test_enforce_minimum_key_length_raises_InvalidKeyError():
    # Setup a concrete alg_obj that reports a short key length
    class ShortKeyAlg:
        def check_key_length(self, key):
            return "too short for this algorithm"
        def prepare_key(self, key):
            return key
        def verify(self, msg, key, sig):
            return True

    alg_obj = ShortKeyAlg()
    pyjws = _make_pyjws_with_alg(alg_name="RS256", enforce_minimum=True, alg_obj=alg_obj)

    signing_input = b"message"
    header = {"alg": "RS256"}
    signature = b"signature"

    with pytest.raises(InvalidKeyError) as exc:
        pyjws._verify_signature(signing_input, header, signature, key=b"key", algorithms=["RS256"])
    assert "too short" in str(exc.value)
