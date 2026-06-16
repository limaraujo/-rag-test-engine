from repositorios.pyjwt.jwt.exceptions import InvalidAlgorithmError, InvalidKeyError, InvalidSignatureError
import pytest
import warnings
from repositorios.pyjwt.jwt.api_jws import PyJWS


# Test 1: missing alg or invalid alg should raise InvalidAlgorithmError
@pytest.mark.parametrize(
    "header, key, algorithms, expected_message",
    [
        ({}, b"secret", None, "Algorithm not specified"),
        ({"alg": ""}, b"secret", ["HS256"], "The specified alg value is not allowed"),
    ],
)
def test_missing_or_invalid_algorithm_raises_InvalidAlgorithmError(header, key, algorithms, expected_message):
    class DummySelf:
        def __init__(self):
            self.options = {}

        def get_algorithm_by_name(self, alg):
            raise NotImplementedError

    with pytest.raises(InvalidAlgorithmError) as exc:
        PyJWS._verify_signature(
            DummySelf(),
            signing_input=b"data",
            header=header,
            signature=b"sig",
            key=key,
            algorithms=algorithms,
            options=None,
        )
    assert expected_message in str(exc.value)


# Test 2: unsupported algorithm name should raise InvalidAlgorithmError
def test_algorithm_not_supported_path_raises_InvalidAlgorithmError():
    class DummySelfNotSupported:
        def __init__(self):
            self.options = {}

        def get_algorithm_by_name(self, alg):
            raise NotImplementedError("not supported")

    with pytest.raises(InvalidAlgorithmError) as exc:
        PyJWS._verify_signature(
            DummySelfNotSupported(),
            signing_input=b"data",
            header={"alg": "HS256"},
            signature=b"sig",
            key=b"secret",
            algorithms=None,
            options=None,
        )
    assert "Algorithm not supported" in str(exc.value)


# Test 3: signature verification flow (success and failure)
@pytest.mark.parametrize("signature, expect_exception", [(b"valid", False), (b"invalid", True)])
def test_signature_verification_flow(signature, expect_exception):
    class FakeAlg:
        algorithm_name = "HS256"

        def check_key_length(self, prepared_key):
            return None

        def prepare_key(self, key):
            return key

        def verify(self, signing_input, prepared_key, sig):
            return sig == b"valid"

    class DummySelf:
        def __init__(self):
            self.options = {}

        def get_algorithm_by_name(self, alg):
            return FakeAlg()

    if expect_exception:
        with pytest.raises(InvalidSignatureError):
            PyJWS._verify_signature(
                DummySelf(),
                signing_input=b"data",
                header={"alg": "HS256"},
                signature=signature,
                key=b"secret",
                algorithms=None,
                options=None,
            )
    else:
        PyJWS._verify_signature(
            DummySelf(),
            signing_input=b"data",
            header={"alg": "HS256"},
            signature=signature,
            key=b"secret",
            algorithms=None,
            options=None,
        )


# Test 4: minimum key length handling - enforce raises, or warns when not enforced
@pytest.mark.parametrize("enforce_min_length, expect_exception", [(True, True), (False, False)])
def test_minimum_key_length_handling(enforce_min_length, expect_exception):
    class FakeAlgLen:
        algorithm_name = "HS256"

        def check_key_length(self, prepared_key):
            return "too short"  # trigger length warning / error

        def prepare_key(self, key):
            return key

        def verify(self, signing_input, prepared_key, signature):
            return True

    class DummySelfLen:
        def __init__(self, options):
            self.options = options

        def get_algorithm_by_name(self, alg):
            return FakeAlgLen()

    dummy = DummySelfLen({"enforce_minimum_key_length": enforce_min_length})

    if expect_exception:
        with pytest.raises(InvalidKeyError):
            PyJWS._verify_signature(
                dummy,
                signing_input=b"data",
                header={"alg": "HS256"},
                signature=b"sig",
                key=b"short",
                algorithms=None,
                options=None,
            )
    else:
        with pytest.warns(Warning):
            PyJWS._verify_signature(
                dummy,
                signing_input=b"data",
                header={"alg": "HS256"},
                signature=b"sig",
                key=b"short",
                algorithms=None,
                options=None,
            )
