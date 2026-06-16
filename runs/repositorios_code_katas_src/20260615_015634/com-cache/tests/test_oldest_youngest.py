import pytest
from repositorios.code_katas.src.forbes import oldest_youngest

# teste feliz: verifica caminho happy path com várias idades válidas e entradas filtradas
def test_oldest_youngest_happy_path(monkeypatch):
    data = {
        "billionaires": [
            {"name": "Alice", "age": 34, "source": "Tech", "net_worth (USD)": 100},
            {"name": "Bob", "age": 60, "source": "Finance", "net_worth (USD)": 200},
            {"name": "Charlie", "age": 70, "source": "Energy", "net_worth (USD)": 300},
            {"name": "Diana", "age": 25, "source": "Retail", "net_worth (USD)": 400},
            {"name": "Eve", "age": 80, "source": "Tech", "net_worth (USD)": 500},   # deve ser filtrada
            {"name": "Frank", "age": -5, "source": "Tech", "net_worth (USD)": 600},   # deve ser filtrada
        ]
    }
    monkeypatch.setattr('repositorios.code_katas.src.forbes.get_json', lambda: data)

    oldest, youngest = oldest_youngest()

    assert oldest[0] == "Charlie"
    assert oldest[1]["age"] == 70
    assert oldest[1]["industry"] == "Energy"
    assert oldest[1]["net worth"] == 300

    assert youngest[0] == "Diana"
    assert youngest[1]["age"] == 25
    assert youngest[1]["industry"] == "Retail"
    assert youngest[1]["net worth"] == 400

# teste de borda: apenas uma entrada válida -> ambos oldest e youngest devem ser a mesma
def test_oldest_youngest_only_one_valid(monkeypatch):
    data = {
        "billionaires": [
            {"name": "OnlyOne", "age": 30, "source": "Tech", "net_worth (USD)": 123},
            {"name": "Ignored", "age": 85, "source": "Finance", "net_worth (USD)": 999}
        ]
    }
    monkeypatch.setattr('repositorios.code_katas.src.forbes.get_json', lambda: data)

    oldest, youngest = oldest_youngest()

    assert oldest[0] == "OnlyOne"
    assert oldest[1]["age"] == 30
    assert oldest[1]["industry"] == "Tech"
    assert oldest[1]["net worth"] == 123

    assert youngest[0] == "OnlyOne"
    assert youngest[1]["age"] == 30
    assert youngest[1]["industry"] == "Tech"
    assert youngest[1]["net worth"] == 123

# teste de exceção: nenhuma entrada válida leva a ValueError ao tentar usar max/min
def test_oldest_youngest_empty_after_filter_raises(monkeypatch):
    data = {
        "billionaires": [
            {"name": "A", "age": 80, "source": "Tech", "net_worth (USD)": 50},
            {"name": "B", "age": -1, "source": "Tech", "net_worth (USD)": 60}
        ]
    }
    monkeypatch.setattr('repositorios.code_katas.src.forbes.get_json', lambda: data)

    with pytest.raises(ValueError):
        oldest_youngest()

# teste de exceção: chave esperada ausente gera KeyError
def test_oldest_youngest_missing_billionaires_key_raises(monkeypatch):
    data = {"not_billionaries": []}
    monkeypatch.setattr('repositorios.code_katas.src.forbes.get_json', lambda: data)

    with pytest.raises(KeyError):
        oldest_youngest()
