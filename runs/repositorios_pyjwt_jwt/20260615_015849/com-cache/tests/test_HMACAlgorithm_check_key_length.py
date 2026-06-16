import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm



class _DummySelf:
    def __init__(self, digest_size: int, name: str):
        class _HashAlg:
            def __init__(self, digest_size, name):
                self.digest_size = digest_size
                self.name = name

        self._hash_alg = _HashAlg(digest_size, name)

    def hash_alg(self):
        return self._hash_alg


# Teste: caminho feliz - chave no tamanho mínimo
def test_check_key_length_happy_path_exact_min():
    dummy = _DummySelf(digest_size=32, name="sha256")
    key = b"a" * 32
    assert HMACAlgorithm.check_key_length(dummy, key) is None


# Teste: exceção - chave abaixo do mínimo retorna mensagem com detalhes
def test_check_key_length_below_min_returns_message():
    dummy = _DummySelf(digest_size=32, name="sha256")
    key = b"a" * 31
    msg = HMACAlgorithm.check_key_length(dummy, key)
    assert isinstance(msg, str)
    assert "31 bytes long" in msg
    assert "minimum recommended length of 32 bytes" in msg
    assert "SHA256" in msg
    assert "RFC 7518 Section 3.2" in msg


# Teste: variação de algoritmo - usa sha1 e chave curta valida formatação
def test_check_key_length_other_hash_short_key():
    dummy = _DummySelf(digest_size=20, name="sha1")
    key = b"abcd"  # 4 bytes
    msg = HMACAlgorithm.check_key_length(dummy, key)
    assert "4 bytes long" in msg
    assert "minimum recommended length of 20 bytes" in msg
    assert "SHA1" in msg


# Teste de borda/afirma: chave maior que mínimo retorna None
def test_check_key_length_longer_key_returns_none():
    dummy = _DummySelf(digest_size=16, name="md5")
    key = b"x" * 20
    assert HMACAlgorithm.check_key_length(dummy, key) is None
