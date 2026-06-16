from repositorios.code_katas.src.forbes import oldest_youngest

# verifica caminho feliz: filtra entradas inválidas e retorna oldest/youngest corretos
def test_oldest_youngest_happy_path_filters_invalid_ages(monkeypatch):
    data = {
        "billionaires": [
            {"name": "Alice", "age": 75, "source": "Tech", "net_worth (USD)": 1000000},
            {"name": "Bob", "age": 82, "source": "Investments", "net_worth (USD)": 1500000},
            {"name": "Charlie", "age": 50, "source": "Energy", "net_worth (USD)": 700000},
            {"name": "Diana", "age": -5, "source": "Retail", "net_worth (USD)": 200000},
            {"name": "Eve", "age": 30, "source": "Media", "net_worth (USD)": 900000}
        ]
    }
    monkeypatch.setattr("repositorios.code_katas.src.forbes.get_json", lambda: data)
    oldest, youngest = oldest_youngest()
    assert oldest[0] == "Alice"
    assert oldest[1]["age"] == 75
    assert oldest[1]["industry"] == "Tech"
    assert youngest[0] == "Eve"
    assert youngest[1]["age"] == 30
    assert youngest[1]["industry"] == "Media"

# verifica cenário com todos os valores válidos para confirmar seleção correta
def test_oldest_youngest_all_valid_ages_next_case(monkeypatch):
    data = {
        "billionaires": [
            {"name": "Xander", "age": 40, "source": "Tech", "net_worth (USD)": 1000000},
            {"name": "Yara", "age": 35, "source": "Finance", "net_worth (USD)": 2000000},
            {"name": "Zoe", "age": 65, "source": "Healthcare", "net_worth (USD)": 3000000},
            {"name": "Will", "age": 25, "source": "Media", "net_worth (USD)": 4000000}
        ]
    }
    monkeypatch.setattr("repositorios.code_katas.src.forbes.get_json", lambda: data)
    oldest, youngest = oldest_youngest()
    assert oldest[0] == "Zoe"
    assert oldest[1]["age"] == 65
    assert oldest[1]["industry"] == "Healthcare"
    assert youngest[0] == "Will"
    assert youngest[1]["age"] == 25
    assert youngest[1]["industry"] == "Media"
