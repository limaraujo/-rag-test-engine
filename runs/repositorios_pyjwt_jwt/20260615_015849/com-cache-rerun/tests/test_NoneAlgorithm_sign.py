import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# short: happy path - sign should return empty bytes regardless of input
@pytest.mark.parametrize("msg", [b"", b"hello", b"\x00" * 64])
def test_none_algorithm_sign_returns_empty_for_various_msgs(msg):
    alg = NoneAlgorithm()
    assert alg.sign(msg, key=None) == b""
