import pytest
import repositorios.code_katas.src.forbes as forbes
from repositorios.code_katas.src.forbes import oldest_youngest

# curto: happy path - verifica que oldest_youngest retorna a mais velha (78) e a mais jovem (6) entre os filtrados
def test_oldest_youngest_happy_path(monkeypatch):
    data = {
        "billionaires": [
            {"name": "Alice", "age": 55, "source": "Tech", "net_worth (USD)": 5},
            {"name": "Bob", "age": 70, "source": "Finance", "net_worth (USD)": 3},
            {"name": "Carol", "age": 78, "source": "Energy", "net_worth (USD)": 8},
            {"name": "Dave", "age": 82, "source": "Retail", "net_worth (USD)": 2},
            {"name": "Eve", "age": 6, "source": "Tech", "net_worth (USD)": 1},
        ]
    }
    monkeypatch.setattr(forbes, "get_json", lambda: data)
    oldest, youngest = forbes.oldest_youngest()
    assert oldest[0] == "Carol"
    assert oldest[1]["age"] == 78
    assert youngest[0] == "Eve"
    assert youngest[1]["age"] == 6
    assert oldest[1]["industry"] == "Energy"
    assert oldest[1]["net worth"] == 8

# curto: borda/limites - verifica filtragem com idade exatamente 80 e negativa (devem ser ignoradas)
def test_oldest_youngest_boundaries(monkeypatch):
    data = {
        "billionaires": [
            {"name": "X", "age": 80, "source": "Tech", "net_worth (USD)": 10},
            {"name": "Y", "age": -5, "source": "Tech", "net_worth (USD)": 15},
            {"name": "Z", "age": 79, "source": "Finance", "net_worth (USD)": 20},
        ]
    }
    monkeypatch.setattr(forbes, "get_json", lambda: data)
    oldest, youngest = forbes.oldest_youngest()
    assert oldest[0] == "Z"
    assert oldest[1]["age"] == 79
    assert youngest[0] == "Z"
    assert youngest[1]["age"] == 79

# curto: exceção/erro - quando nenhum candidato atende ao filtro, max()/min() geram erro
def test_oldest_youngest_no_candidates_raises(monkeypatch):
    data = {
        "billionaires": [
            {"name": "A", "age": 80, "source": "Tech", "net_worth (USD)": 5},
            {"name": "B", "age": -1, "source": "Tech", "net_worth (USD)": 6},
        ]
    }
    monkeypatch.setattr(forbes, "get_json", lambda: data)
    with pytest.raises(ValueError):
        forbes.oldest_youngest()
