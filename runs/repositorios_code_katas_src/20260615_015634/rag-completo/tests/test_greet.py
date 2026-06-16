from repositorios.code_katas.src.jenny import greet

# Verifica branch: nome é "Johnny" retorna o cumprimento especial
def test_greet_johnny():
    assert greet("Johnny") == "Hello, my love!"

# Verifica branch: nome diferente de "Johnny" retorna cumprimento normal com o nome
def test_greet_other():
    assert greet("Alice") == "Hello, Alice!"
