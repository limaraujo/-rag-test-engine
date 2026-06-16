from repositorios.code_katas.src.jenny import greet

# Teste: branch true - checa o cumprimento especial para "Johnny"
def test_greet_Johnny_returns_special():
    assert greet("Johnny") == "Hello, my love!"

# Teste: branch false - checa o cumprimento normal para outro nome
def test_greet_other_name_returns_normal():
    assert greet("Alice") == "Hello, Alice!"

# Teste de borda: nome vazio ainda usa o caminho normal
def test_greet_empty_string_returns_normal():
    assert greet("") == "Hello, !"
