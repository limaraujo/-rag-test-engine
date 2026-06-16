import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Verifica remoção bem-sucedida de algoritmo existente (caminho feliz)
def test_unregister_algorithm_removes_existing_algorithm():
    # cria instância sem chamar o __init__ para evitar dependências
    obj = PyJWS.__new__(PyJWS)
    obj._algorithms = {'RS256': object()}
    obj._valid_algs = ['RS256']

    obj.unregister_algorithm('RS256')

    assert 'RS256' not in obj._algorithms
    assert 'RS256' not in obj._valid_algs

# Verifica lançamento de KeyError quando o algoritmo não está registrado (exceção esperada)
def test_unregister_algorithm_raises_keyerror_when_missing():
    obj = PyJWS.__new__(PyJWS)
    obj._algorithms = {}
    obj._valid_algs = []

    with pytest.raises(KeyError):
        obj.unregister_algorithm('HS256')
