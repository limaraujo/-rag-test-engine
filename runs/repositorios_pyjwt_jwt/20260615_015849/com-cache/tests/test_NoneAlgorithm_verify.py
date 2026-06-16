from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm


# happy path: verify() always returns False for typical inputs
def test_nonealgorithm_verify_happy_path():
    algo = NoneAlgorithm()
    assert algo.verify(msg=b"hello", key=None, sig=b"signature") is False


# edge case: verify() with empty inputs
def test_nonealgorithm_verify_empty_inputs():
    algo = NoneAlgorithm()
    assert algo.verify(msg=b"", key=None, sig=b"") is False


# boundary: verify() with large inputs
def test_nonealgorithm_verify_large_inputs():
    algo = NoneAlgorithm()
    msg = b"a" * 1024
    sig = b"b" * 512
    assert algo.verify(msg=msg, key=None, sig=sig) is False
