import importlib
import pytest
from repositorios.code_katas.src.forbes import oldest_youngest

MOD_PATH = "repositorios.code_katas.src.forbes"

# Verifica caminho feliz: múltiplos dados válidos, calcula maior e menor idade corretamente
def test_oldest_youngest_happy_path(monkeypatch):
    mod = importlib.import_module(MOD_PATH)
    data = {
        "billionaires": [
            {"name": "Charlie", "age": 77, "source": "Healthcare", "net_worth (USD)": 800},
            {"name": "Alice", "age": 45, "source": "Tech", "net_worth (USD)": 1000},
            {"name": "Bob", "age": 30, "source": "Finance", "net_worth (USD)": 400},
            {"name": "Dave", "age": 15, "source": "Retail", "net_worth (USD)": 50},
        ]
    }
    monkeypatch.setattr(mod, "get_json", lambda: data)
    oldest, youngest = mod.oldest_youngest()
    assert oldest[0] == "Charlie"
    assert youngest[0] == "Dave"
    assert oldest[1]["industry"] == "Healthcare"
    assert youngest[1]["net worth"] == 50

# Verifica inclusão de limites 0 e 79
def test_oldest_youngest_boundaries(monkeypatch):
    mod = importlib.import_module(MOD_PATH)
    data = {
        "billionaires": [
            {"name": "X", "age": 0, "source": "A", "net_worth (USD)": 10},
            {"name": "Y", "age": 79, "source": "B", "net_worth (USD)": 20}
        ]
    }
    monkeypatch.setattr(mod, "get_json", lambda: data)
    oldest, youngest = mod.oldest_youngest()
    assert oldest[0] == "Y"
    assert youngest[0] == "X"

# Verifica comportamento quando nenhum item está no intervalo permitido (lança ValueError)
def test_oldest_youngest_empty_after_filter_raises(monkeypatch):
    mod = importlib.import_module(MOD_PATH)
    data = {
        "billionaires": [
            {"name": "A", "age": 80, "source": "S", "net_worth (USD)": 100},
            {"name": "B", "age": -5, "source": "S", "net_worth (USD)": 200}
        ]
    }
    monkeypatch.setattr(mod, "get_json", lambda: data)
    with pytest.raises(ValueError):
        mod.oldest_youngest()

# Verifica combinação de casos de borda com múltiplos itens, assegurando mapeamento correto
def test_oldest_youngest_multiple_corners(monkeypatch):
    mod = importlib.import_module(MOD_PATH)
    data = {
        "billionaires": [
            {"name": "Grace", "age": 10, "source": "Retail", "net_worth (USD)": 40},
            {"name": "Eve", "age": 60, "source": "Energy", "net_worth (USD)": 500},
            {"name": "Frank", "age": 70, "source": "Tech", "net_worth (USD)": 900}
        ]
    }
    monkeypatch.setattr(mod, "get_json", lambda: data)
    oldest, youngest = mod.oldest_youngest()
    assert oldest[0] == "Frank"
    assert youngest[0] == "Grace"
