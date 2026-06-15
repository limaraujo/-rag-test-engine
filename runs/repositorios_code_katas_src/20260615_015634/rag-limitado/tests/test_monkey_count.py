from repositorios.code_katas.src.monkey import monkey_count

# happy path: n=5 retorna [1,2,3,4,5]
def test_monkey_count_happy_path():
    assert monkey_count(5) == [1, 2, 3, 4, 5]

# borda: n=0 retorna lista vazia
def test_monkey_count_zero_returns_empty():
    assert monkey_count(0) == []

# borda: n negativo retorna lista vazia
def test_monkey_count_negative_returns_empty():
    assert monkey_count(-3) == []

# grande n: verifica sequencia até 1000
def test_monkey_count_large_n():
    assert monkey_count(1000) == list(range(1, 1001))
