import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm


# curto
class DummyHash:
    def __init__(self, digest_size: int, name: str):
        self.digest_size = digest_size
        self.name = name

# curto
def test_check_key_length_returns_error_for_short_key():
    min_length = 16
    dummy = DummyHash(digest_size=min_length, name="sha256")
    alg = object.__new__(HMACAlgorithm)
    alg.hash_alg = lambda: dummy

    key = b"a" * 8
    expected = (
        f"The HMAC key is {len(key)} bytes long, which is below "
        f"the minimum recommended length of {min_length} bytes for "
        f"{dummy.name.upper()}. "
        "See RFC 7518 Section 3.2."
    )

    result = alg.check_key_length(key)
    assert result == expected

# curto
@pytest.mark.parametrize("key_len", [16, 32])
def test_check_key_length_returns_none_for_sufficient_key(key_len):
    min_length = 16
    dummy = DummyHash(digest_size=min_length, name="sha256")
    alg = object.__new__(HMACAlgorithm)
    alg.hash_alg = lambda: dummy

    key = b"a" * key_len
    result = alg.check_key_length(key)
    assert result is None
