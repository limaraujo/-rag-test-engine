from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

class DummyHMACAlgorithm(HMACAlgorithm):
    def __init__(self, digest_size: int, name: str):
        self._digest_size = digest_size
        self._name = name

    def hash_alg(self):
        class HashObj:
            def __init__(self, digest_size, name):
                self.digest_size = digest_size
                self.name = name
        return HashObj(self._digest_size, self._name)

# curto: happy path - key length exactly at the minimum returns None
def test_check_key_length_happy_path():
    alg = DummyHMACAlgorithm(digest_size=32, name='sha256')
    key = b'a' * 32
    assert alg.check_key_length(key) is None

# curto: borda/baixo do mínimo - key length below min_length returns informative message
def test_check_key_length_below_minimum():
    alg = DummyHMACAlgorithm(digest_size=16, name='sha256')
    key = b'a' * 5
    expected = (
        "The HMAC key is 5 bytes long, which is below the minimum recommended length of 16 bytes for "
        "SHA256. See RFC 7518 Section 3.2."
    )
    assert alg.check_key_length(key) == expected
