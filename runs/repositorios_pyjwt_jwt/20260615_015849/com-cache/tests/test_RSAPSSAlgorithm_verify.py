from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm

# curto: happy path – assinatura válida não levanta exceção e retorna True
def test_verify_true_on_valid_signature():
    # cria instância do objeto sem chamar __init__
    algo = object.__new__(RSAPSSAlgorithm)
    # força hash usado pelo RSAPSSAlgorithm
    algo.hash_alg = lambda: hashes.SHA256()

    class DummyKey:
        def __init__(self, raise_on_verify=False):
            self.raise_on_verify = raise_on_verify
            self.called_with = None

        def verify(self, sig, msg, padding_arg, hash_alg_arg):
            self.called_with = (sig, msg, padding_arg, hash_alg_arg)
            if self.raise_on_verify:
                raise InvalidSignature()

    key = DummyKey(raise_on_verify=False)
    msg = b"sample message"
    sig = b"signature"

    assert RSAPSSAlgorithm.verify(algo, msg, key, sig) is True
    # Verifica que o verify recebeu os parâmetros esperados
    assert key.called_with[0] == sig
    assert key.called_with[1] == msg
    # O terceiro/quarto argumentos são objetos do padding/hash usados
    assert key.called_with[2] is not None
    assert key.called_with[3] is not None

# curto: exceção InvalidSignature é lançada – o método retorna False
def test_verify_false_on_invalid_signature():
    algo = object.__new__(RSAPSSAlgorithm)
    algo.hash_alg = lambda: hashes.SHA256()

    class DummyKey:
        def __init__(self, raise_on_verify=False):
            self.raise_on_verify = raise_on_verify
            self.called_with = None

        def verify(self, sig, msg, padding_arg, hash_alg_arg):
            self.called_with = (sig, msg, padding_arg, hash_alg_arg)
            if self.raise_on_verify:
                raise InvalidSignature()

    key = DummyKey(raise_on_verify=True)
    msg = b"sample message"
    sig = b"signature"

    assert RSAPSSAlgorithm.verify(algo, msg, key, sig) is False
    # Verifica que o verify foi de fato chamado
    assert key.called_with[0] == sig
    assert key.called_with[1] == msg
