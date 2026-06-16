from unittest.mock import Mock
import pytest
import warnings
from repositorios.pyjwt.jwt.api_jwt import PyJWT



# helper to create a PyJWT instance with mocked internals
def _make_jwt_with_mocks():
    jwt_obj = PyJWT.__new__(PyJWT)
    mock_jws = Mock()
    mock_jws.decode_complete.return_value = {'header': 'H', 'payload': 'P', 'signature': 'S'}
    jwt_obj._jws = mock_jws
    jwt_obj._decode_payload = Mock(return_value='payload_decoded')
    jwt_obj._validate_claims = Mock()
    jwt_obj._merge_options = Mock(return_value={'enforce_minimum_key_length': False})
    return jwt_obj


# curto: happy path - valida retorno completo com payload decodificado
def test_decode_complete_happy_path():
    jwt_obj = _make_jwt_with_mocks()

    decoded = jwt_obj.decode_complete("token", key="key", algorithms=["HS256"])

    assert decoded == {'header': 'H', 'payload': 'payload_decoded', 'signature': 'S'}
    jwt_obj._jws.decode_complete.assert_called_once_with(
        "token",
        key="key",
        algorithms=["HS256"],
        options={'verify_signature': True, 'enforce_minimum_key_length': False},
        detached_payload=None,
    )


# curto: verify_signature flag é respeitado quando fornecido em options
def test_decode_complete_respects_verify_signature_option():
    jwt_obj = _make_jwt_with_mocks()

    decoded = jwt_obj.decode_complete("token", key="key", algorithms=["HS256"], options={"verify_signature": False})

    assert decoded == {'header': 'H', 'payload': 'payload_decoded', 'signature': 'S'}
    jwt_obj._jws.decode_complete.assert_called_once_with(
        "token",
        key="key",
        algorithms=["HS256"],
        options={'verify_signature': False, 'enforce_minimum_key_length': False},
        detached_payload=None,
    )


# curto: aviso ao passar kwargs adicionais (kwargs não suportados) para decode_complete
def test_decode_complete_warns_on_extra_kwargs():
    jwt_obj = _make_jwt_with_mocks()

    with pytest.warns(Warning):
        jwt_obj.decode_complete("token", key="key", algorithms=["HS256"], foo="bar")
