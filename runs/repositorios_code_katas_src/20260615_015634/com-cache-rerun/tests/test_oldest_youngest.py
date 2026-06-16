import pytest
import repositorios.code_katas.src.forbes as Forbes
from repositorios.code_katas.src.forbes import oldest_youngest

# teste feliz: verifica caminho happy path com filtering de entradas não elegíveis
def test_oldest_youngest_happy_path(monkeypatch):
    data = {
        "billionaires": [
            {"name": "Alice", "age": 30, "source": "Tech", "net_worth (USD)": 1000},
            {"name": "Bob", "age": 70, "source": "Finance", "net_worth (USD)": 1500},
            {"name": "Carol", "age": 85, "source": "Media", "net_worth (USD)": 1200},  # filtrada (>=80)
            {"name": "Dave", "age": 25, "source": "Retail", "net_worth (USD)": 600},
            {"name": "Eve", "age": -5, "source": "Tech", "net_worth (USD)": 400},  # filtrada (<0)
        ]
    }
    def fake_get_json():
        return data
    monkeypatch.setattr(Forbes, "get_json", fake_get_json)

    oldest, youngest = oldest_youngest()
    assert oldest[0] == "Bob"
    assert oldest[1]["age"] == 70
    assert oldest[1]["industry"] == "Finance"
    assert oldest[1]["net worth"] == 1500

    assert youngest[0] == "Dave"
    assert youngest[1]["age"] == 25
    assert youngest[1]["industry"] == "Retail"
    assert youngest[1]["net worth"] == 600

# teste de borda/exceção: quando todas as entradas são filtradas, max()/min() falham
def test_oldest_youngest_all_filtered_raises(monkeypatch):
    data = {
        "billionaires": [
            {"name": "X", "age": 80, "source": "A", "net_worth (USD)": 1000},
            {"name": "Y", "age": 90, "source": "B", "net_worth (USD)": 1200}
        ]
    }
    monkeypatch.setattr(Forbes, "get_json", lambda: data)

    with pytest.raises(ValueError):
        oldest_youngest()

# teste de borda: apenas uma entrada elegível retorna a mesma para oldest e youngest
def test_oldest_youngest_single_entry(monkeypatch):
    data = {
        "billionaires": [
            {"name": "Solo", "age": 55, "source": "Tech", "net_worth (USD)": 300},
            {"name": "Oldie", "age": 85, "source": "Tech", "net_worth (USD)": 900}  # filtrada
        ]
    }
    monkeypatch.setattr(Forbes, "get_json", lambda: data)

    oldest, youngest = oldest_youngest()
    assert oldest[0] == "Solo"
    assert youngest[0] == "Solo"
    assert oldest[1]["age"] == 55
    assert youngest[1]["age"] == 55
