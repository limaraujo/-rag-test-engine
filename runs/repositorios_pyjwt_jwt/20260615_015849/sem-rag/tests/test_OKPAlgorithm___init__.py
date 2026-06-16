import pytest
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# Testa o caminho feliz: inicialização sem kwargs não levanta exceção
def test_okp_algorithm_init_happy_path_no_kwargs():
    alg = OKPAlgorithm()
    assert isinstance(alg, OKPAlgorithm)

# Testa aceitação de um único kwargs: o __init__ deve aceitar sem raise
def test_okp_algorithm_init_accepts_single_kwarg():
    alg = OKPAlgorithm(foo='bar')
    assert isinstance(alg, OKPAlgorithm)

# Testa aceitação de múltiplos kwargs: o __init__ deve aceitar sem raise
def test_okp_algorithm_init_accepts_multiple_kwargs():
    alg = OKPAlgorithm(bar=1, baz=[1, 2, 3], qux={'a': 1})
    assert isinstance(alg, OKPAlgorithm)
