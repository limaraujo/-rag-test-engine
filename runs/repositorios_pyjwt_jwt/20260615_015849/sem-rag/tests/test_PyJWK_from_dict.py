from unittest.mock import patch
from repositorios.pyjwt.jwt.api_jwk import PyJWK

# Verifica o caminho feliz: from_dict cria PyJWK com obj e algoritmo default None
def test_from_dict_happy_path_default_algorithm():
    obj = {'kty': 'oct'}
    def fake_init(self, obj_in, algorithm=None):
        self._captured = (obj_in, algorithm)
    with patch.object(PyJWK, '__init__', new=fake_init):
        jwk = PyJWK.from_dict(obj)
    assert isinstance(jwk, PyJWK)
    assert getattr(jwk, '_captured', None) == (obj, None)

# Verifica que from_dict passa o algoritmo explícito para PyJWK.__init__
def test_from_dict_with_explicit_algorithm():
    obj = {'kty': 'oct'}
    alg = 'RS256'
    def fake_init(self, obj_in, algorithm=None):
        self._captured = (obj_in, algorithm)
    with patch.object(PyJWK, '__init__', new=fake_init):
        jwk = PyJWK.from_dict(obj, algorithm=alg)
    assert getattr(jwk, '_captured', None) == (obj, alg)
