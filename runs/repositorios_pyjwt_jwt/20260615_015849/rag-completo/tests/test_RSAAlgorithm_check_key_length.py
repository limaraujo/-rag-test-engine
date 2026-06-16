from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

class DummyKey:
    def __init__(self, key_size: int) -> None:
        self.key_size = key_size

# curto: verifica branch onde key_size é menor que o mínimo esperado
def test_check_key_length_below_minimum_returns_error_string():
    algo = RSAAlgorithm.__new__(RSAAlgorithm)
    min_size = getattr(algo, "_MIN_KEY_SIZE", None)
    if min_size is None:
        min_size = 2048
        setattr(algo, "_MIN_KEY_SIZE", min_size)
    key = DummyKey(min_size - 1)
    result = RSAAlgorithm.check_key_length(algo, key)
    assert isinstance(result, str)
    assert str(key.key_size) in result
    assert str(min_size) in result
    assert "NIST SP 800-131A" in result

# curto: verifica branch onde key_size >= mínimo retorna None
def test_check_key_length_at_or_above_minimum_returns_none():
    algo = RSAAlgorithm.__new__(RSAAlgorithm)
    min_size = getattr(algo, "_MIN_KEY_SIZE", None)
    if min_size is None:
        min_size = 2048
        setattr(algo, "_MIN_KEY_SIZE", min_size)
    key = DummyKey(min_size)
    result = RSAAlgorithm.check_key_length(algo, key)
    assert result is None
