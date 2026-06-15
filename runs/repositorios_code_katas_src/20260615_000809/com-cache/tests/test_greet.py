from repositorios.code_katas.src.jenny import greet

# Verifica saudação especial para Johnny (branch verdadeira)
def test_greet_special_case_johnny():
    assert greet("Johnny") == "Hello, my love!"

# Verifica saudação padrão para outro nome (branch falsa)
def test_greet_default_case_other():
    assert greet("Ada") == "Hello, Ada!"
