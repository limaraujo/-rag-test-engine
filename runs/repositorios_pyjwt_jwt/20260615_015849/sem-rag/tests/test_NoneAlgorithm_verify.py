from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# teste: happy path - verifica que verify retorna False com entradas típicas
def test_verify_always_false_basic():
    alg = NoneAlgorithm()
    assert alg.verify(msg=b"hello", key=None, sig=b"signature") is False

# teste: caso de borda - assinatura vazia ainda retorna False
def test_verify_always_false_empty_signature():
    alg = NoneAlgorithm()
    assert alg.verify(msg=b"message", key=None, sig=b"") is False

# teste: robustez - tipos não-bytes são aceitos pela assinatura e retornam False
def test_verify_always_false_non_bytes_inputs():
    alg = NoneAlgorithm()
    assert alg.verify(msg="notbytes", key=123, sig=None) is False
