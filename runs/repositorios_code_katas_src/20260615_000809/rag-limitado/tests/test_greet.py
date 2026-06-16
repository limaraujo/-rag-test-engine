from repositorios.code_katas.src.jenny import greet

# curto: verifica branch quando name é "Johnny" (resposta especial)
def test_greet_johnny_special():
    assert greet("Johnny") == "Hello, my love!"

# curto: verifica caminho principal para nomes diferentes de Johnny (happy path)
def test_greet_other_name_happy_path():
    assert greet("Alice") == "Hello, Alice!"
