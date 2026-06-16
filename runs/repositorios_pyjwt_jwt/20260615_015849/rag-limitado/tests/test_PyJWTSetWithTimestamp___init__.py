import time
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# Verifica caminho feliz: atribuição de jwk_set e timestamp com monotonic fixo
def test_init_sets_jwk_set_and_timestamp_with_fixed_monotonic(monkeypatch):
    fixed = 7.5
    def fake_monotonic():
        return fixed

    monkeypatch.setattr(time, 'monotonic', fake_monotonic)
    dummy_jwk_set = object()
    obj = PyJWTSetWithTimestamp(dummy_jwk_set)
    assert obj.jwk_set is dummy_jwk_set
    assert obj.timestamp == fixed

# Verifica que time.monotonic é chamado exatamente uma vez ao inicializar
def test_init_calls_monotonic_once(monkeypatch):
    calls = {'n': 0}
    def fake_monotonic():
        calls['n'] += 1
        return 12.34

    monkeypatch.setattr(time, 'monotonic', fake_monotonic)
    dummy = object()
    obj = PyJWTSetWithTimestamp(dummy)
    assert obj.timestamp == 12.34
    assert calls['n'] == 1
    assert obj.jwk_set is dummy
