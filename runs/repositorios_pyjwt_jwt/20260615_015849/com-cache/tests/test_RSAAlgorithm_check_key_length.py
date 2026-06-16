from types import SimpleNamespace
import pytest
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

from types import SimpleNamespace

import pytest
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm


class TestableRSAAlgorithm(RSAAlgorithm):
    def __init__(self, min_size: int):
        self._MIN_KEY_SIZE = min_size


# Verifica branch: key_size abaixo do mínimo retorna mensagem; caso acima retorna None
@pytest.mark.parametrize("size,min_size", [
    (512, 1024),
    (2048, 1024),
])
def test_check_key_length_branch_and_happy(size, min_size):
    alg = TestableRSAAlgorithm(min_size)
    key = SimpleNamespace(key_size=size)
    result = alg.check_key_length(key)
    if size < min_size:
        expected = f"The RSA key is {size} bits long, which is below the minimum recommended size of {min_size} bits. See NIST SP 800-131A."
        assert result == expected
    else:
        assert result is None
