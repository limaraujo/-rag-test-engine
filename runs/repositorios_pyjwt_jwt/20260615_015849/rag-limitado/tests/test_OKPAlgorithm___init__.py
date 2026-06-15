from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# curto: happy path - inicializa OKPAlgorithm sem argumentos
def test_okp_algorithm_init_no_kwargs():
    alg = OKPAlgorithm()
    assert isinstance(alg, OKPAlgorithm)

# curto: happy path - aceita kwargs arbitrários sem falhar
def test_okp_algorithm_init_with_kwargs():
    alg = OKPAlgorithm(foo="bar", baz=123)
    assert isinstance(alg, OKPAlgorithm)
