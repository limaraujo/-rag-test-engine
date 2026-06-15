import pytest
from repositorios.code_katas.src.forbes import oldest_youngest

# curto
# happy path: verifica seleção correta e ordens com dados mistos (inclui apenas <80 e >=0)


def test_oldest_youngest_happy_path(monkeypatch):
    data = {
        'billionaires': [
            {'name': 'Alice', 'age': 25, 'source': 'Tech', 'net_worth (USD)': 1000000000},
            {'name': 'Bob', 'age': 40, 'source': 'Finance', 'net_worth (USD)': 2000000000},
            {'name': 'Carol', 'age': 70, 'source': 'Energy', 'net_worth (USD)': 5000000000},
            {'name': 'Dave', 'age': 85, 'source': 'Retail', 'net_worth (USD)': 1500000000},
            {'name': 'Eve', 'age': -5, 'source': 'Media', 'net_worth (USD)': 800000000},
        ]
    }

    monkeypatch.setattr('repositorios.code_katas.src.forbes.get_json', lambda: data)
    oldest, youngest = oldest_youngest()

    assert oldest[0] == 'Carol'
    assert oldest[1]['age'] == 70
    assert oldest[1]['industry'] == 'Energy'
    assert oldest[1]['net worth'] == 5000000000

    assert youngest[0] == 'Alice'
    assert youngest[1]['age'] == 25


# curto
# branch: nenhum valor atende aos critérios (gera ValueError)
def test_oldest_youngest_all_excluded_raises(monkeypatch):
    data = {
        'billionaires': [
            {'name': 'X', 'age': 80, 'source': 'Tech', 'net_worth (USD)': 1000000},
            {'name': 'Y', 'age': -1, 'source': 'Tech', 'net_worth (USD)': 2000000},
        ]
    }

    monkeypatch.setattr('repositorios.code_katas.src.forbes.get_json', lambda: data)

    with pytest.raises(ValueError):
        oldest_youngest()


# curto
# edge: idade zero incluída; verifica ordem e mapeamento de campos
def test_oldest_youngest_includes_zero_and_handles_inclusion(monkeypatch):
    data = {
        'billionaires': [
            {'name': 'Zed', 'age': 0, 'source': 'Tech', 'net_worth (USD)': 100},
            {'name': 'Yan', 'age': 60, 'source': 'Healthcare', 'net_worth (USD)': 300},
            {'name': 'Wyn', 'age': 79, 'source': 'Retail', 'net_worth (USD)': 400},
            {'name': 'NotIncluded', 'age': 80, 'source': 'Tech', 'net_worth (USD)': 999},
        ]
    }

    monkeypatch.setattr('repositorios.code_katas.src.forbes.get_json', lambda: data)
    oldest, youngest = oldest_youngest()

    assert oldest[0] == 'Wyn'
    assert oldest[1]['age'] == 79
    assert oldest[1]['industry'] == 'Retail'
    assert oldest[1]['net worth'] == 400

    assert youngest[0] == 'Zed'
    assert youngest[1]['age'] == 0
