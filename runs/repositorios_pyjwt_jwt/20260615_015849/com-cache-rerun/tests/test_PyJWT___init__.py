from unittest.mock import patch
from repositorios.pyjwt.jwt.api_jwt import PyJWT


# verifica caminho feliz (happy path): sem options usa default, gera PyJWS com sig options
def test_init_default_uses_default_options_and_creates_jws():
    with patch.object(PyJWT, "_get_default_options", return_value={"verify_signature": True}) as mock_default:
        with patch.object(PyJWT, "_get_sig_options", return_value={"sig": "X"}) as mock_sig:
            with patch("repositorios.pyjwt.jwt.api_jwt.PyJWS") as mock_pyjws:
                jwt = PyJWT()
                assert jwt.options == {"verify_signature": True}
                mock_default.assert_called_once()
                mock_sig.assert_called_once()
                mock_pyjws.assert_called_once()
                assert mock_pyjws.call_args[1]["options"] == {"sig": "X"}


# verifica caminho com options: merge com _merge_options e usa sig options na PyJWS
def test_init_with_options_merges_and_sets_options_and_creates_jws():
    called_with = []

    def fake_merge(*args, **kwargs):
        opt = args[-1]
        called_with.append(opt)
        return {"verify_signature": False}

    with patch.object(PyJWT, "_get_default_options", return_value={"verify_signature": True}):
        with patch.object(PyJWT, "_get_sig_options", return_value={"sig": "Y"}):
            with patch.object(PyJWT, "_merge_options", side_effect=fake_merge) as mock_merge:
                with patch("repositorios.pyjwt.jwt.api_jwt.PyJWS") as mock_pyjws:
                    jwt = PyJWT(options={"custom": 1})
                    assert jwt.options == {"verify_signature": False}
                    assert called_with == [{"custom": 1}]
                    mock_pyjws.assert_called_once()
                    assert mock_pyjws.call_args[1]["options"] == {"sig": "Y"}
