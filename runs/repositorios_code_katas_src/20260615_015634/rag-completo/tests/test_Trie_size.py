from repositorios.code_katas.src.trietree import Trie

# verifica tamanho inicial em trie vazia
def test_size_initially_zero():
    t = Trie()
    assert t.size() == 0

# verifica tamanho após inserir várias palavras distintas
def test_size_after_multiple_insertions():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    t.insert("cart")
    assert t.size() == 3

# verifica que duplicatas não aumentam o tamanho
def test_size_no_increment_on_duplicate_insertions():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    t.insert("cat")  # duplicata
    t.insert("car")  # duplicata
    assert t.size() == 2

# verifica crescimento de size com novas palavras adicionais
def test_size_after_more_insertions():
    t = Trie()
    for w in ["apple", "banana", "cherry", "date"]:
        t.insert(w)
    assert t.size() == 4
