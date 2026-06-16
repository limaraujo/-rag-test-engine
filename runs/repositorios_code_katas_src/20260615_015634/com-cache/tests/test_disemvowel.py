from repositorios.code_katas.src.disemvowel import disemvowel

# teste feliz: remove vogais de frase comum (happy path)
def test_disemvowel_happy_path_basic():
    input_str = "This is a test"
    expected = "Ths s  tst"
    assert disemvowel(input_str) == expected

# teste borda: string vazia deve permanecer vazia
def test_disemvowel_empty_string():
    assert disemvowel("") == ""

# teste exceção/branch: todas as vogais maiúsculas devem ser removidas
def test_disemvowel_all_uppercase_vowels():
    assert disemvowel("AEIOU") == ""

# teste combinação: pontuação e espaços não são vogais, apenas letras atendem
def test_disemvowel_punctuation_and_numbers():
    input_str = "Hello, World!"
    expected = "Hll, Wrld!"
    assert disemvowel(input_str) == expected
