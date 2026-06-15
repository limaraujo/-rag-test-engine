import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm


class _FakeHashAlg:
    def __init__(self, digest_size: int, name: str):
        self.digest_size = digest_size
        self.name = name


class _FakeSelf:
    def __init__(self, digest_size: int, name: str):
        self._digest_size = digest_size
        self._name = name

    def hash_alg(self) -> _FakeHashAlg:
        return _FakeHashAlg(self._digest_size, self._name)


# Verifica que retorna mensagem de erro quando key é menor que o mínimo recomendado
@pytest.mark.parametrize("digest_size, key_len", [
    (16, 8),
    (32, 31),
])
def test_check_key_length_key_too_short_returns_error(digest_size, key_len):
    fake = _FakeSelf(digest_size=digest_size, name="sha256")
    key = b"a" * key_len
    result = HMACAlgorithm.check_key_length(fake, key)
    assert isinstance(result, str)
    assert f"minimum recommended length of {digest_size} bytes" in result
    assert "SHA256" in result
    assert "RFC 7518" in result  # See RFC 7518 Section 3.2.


# Verifica que não retorna mensagem de erro quando key length é igual ou maior que o mínimo
@pytest.mark.parametrize("digest_size, key_len", [
    (16, 16),
    (32, 33),
])
def test_check_key_length_key_not_short_returns_none(digest_size, key_len):
    fake = _FakeSelf(digest_size=digest_size, name="sha256")
    key = b"b" * key_len
    result = HMACAlgorithm.check_key_length(fake, key)
    assert result is None
