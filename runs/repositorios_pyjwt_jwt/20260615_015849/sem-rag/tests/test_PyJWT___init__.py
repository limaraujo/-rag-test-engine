from unittest.mock import patch
from repositorios.pyjwt.jwt.api_jwt import PyJWT



# Verifica o caminho feliz sem options: usa default options, não chama _merge_options, cria PyJWS com sig options
def test_init_no_options_uses_default_and_creates_pyjws():
    with patch('repositorios.pyjwt.jwt.api_jwt.PyJWS') as MockPyJWS, \
         patch('repositorios.pyjwt.jwt.api_jwt.PyJWT._get_default_options', return_value='default_opts') as mock_default, \
         patch('repositorios.pyjwt.jwt.api_jwt.PyJWT._get_sig_options', return_value='sig_opts') as mock_sig, \
         patch('repositorios.pyjwt.jwt.api_jwt.PyJWT._merge_options') as mock_merge:

        jwt = PyJWT()

        # _merge_options não deve ser chamado nesse caminho
        mock_merge.assert_not_called()
        # self.options deve ser o valor retornado por _get_default_options
        assert jwt.options == 'default_opts'
        # PyJWS deve ser instanciado com as opções vindas de _get_sig_options
        MockPyJWS.assert_called_once_with(options='sig_opts')


# Verifica o caminho com options: mescla options via _merge_options, cria PyJWS com sig options
def test_init_with_options_merges_and_creates_pyjws():
    with patch('repositorios.pyjwt.jwt.api_jwt.PyJWS') as MockPyJWS, \
         patch('repositorios.pyjwt.jwt.api_jwt.PyJWT._get_default_options', return_value='default_opts') as mock_default, \
         patch('repositorios.pyjwt.jwt.api_jwt.PyJWT._get_sig_options', return_value='sig_opts') as mock_sig, \
         patch('repositorios.pyjwt.jwt.api_jwt.PyJWT._merge_options') as mock_merge:

        mock_merge.return_value = 'merged_opts'
        jwt = PyJWT(options={'custom': 'value'})

        # _merge_options deve ter sido chamado com o valor fornecido
        mock_merge.assert_called_once_with({'custom': 'value'})
        # self.options deve ser o valor retornado por _merge_options
        assert jwt.options == 'merged_opts'
        # PyJWS deve ser instanciado com as opções vindas de _get_sig_options
        MockPyJWS.assert_called_once_with(options='sig_opts')
