# Ajuste do RAG

Como melhorar a qualidade do enriquecimento RAG no pipeline de geração de testes.

## Problemas observados (code-katas)

| Sintoma | Causa provável |
|---------|----------------|
| `sem-rag` salvou mais símbolos que `rag-completo` | Snippets vetoriais de outros katas confundem imports |
| `similar_tests=0` no início do run | Coleção de testes vazia até o pipeline salvar aprovados |
| Cache sem hits no lote antigo | Cache limpo antes de `com-cache` (corrigido no protocolo `fair`) |
| RAG piorou `Trie.*` | Contexto irrelevante + reparo sem RAG |

## Melhorias já implementadas no código

### 1. Gating de símbolos triviais (`RAG_SKIP_ISOLATED_SYMBOLS`)

Funções isoladas (sem callers/callees/deps, sem exceções, ≤1 branch, sem classe) **não recebem RAG** — o prompt estático basta.

```env
RAG_SKIP_ISOLATED_SYMBOLS=true
RAG_MIN_BRANCHES_FOR_ENRICHMENT=1
```

### 2. Filtro de score híbrido (`RAG_MIN_HYBRID_SCORE`)

Candidatos **só vetoriais** com score baixo são descartados. Vizinhos de grafo/deps **sempre passam**.

```env
RAG_MIN_HYBRID_SCORE=0.35
```

### 3. Boost mesmo módulo (`RAG_SAME_MODULE_BOOST`)

Símbolos no **mesmo diretório** do alvo ganham bônus no rerank — reduz ruído cross-kata/cross-pacote.

```env
RAG_SAME_MODULE_BOOST=0.15
```

### 4. Limiar separado para testes similares

```env
RETRIEVER_TEST_SCORE_THRESHOLD=0.45
```

Mais permissivo que `RETRIEVER_SCORE_THRESHOLD` (0.55) porque a coleção de testes começa vazia.

### 5. Dedup de seções RAG

Callees/callers/deps **não repetem** em `related_functions`.

### 6. Prompt do gerador

Instruções explícitas: não copiar imports de snippets RAG; priorizar grafo sobre similaridade vetorial.

### 7. Reparo com contexto mínimo

Modo compacto inclui **imports do arquivo** + callees/callers (até 2 snippets) para alinhar geração e reparo.

## Protocolo de avaliação justo

```bash
python scripts/run_all_profiles.py repositorios/code_katas/src
python scripts/compare_run_metrics.py runs/repositorios_code_katas_src/<run_group>
```

- **RAG:** compare `sem-rag` vs `rag-*` vs 1ª `com-cache` (cache frio entre perfis RAG).
- **Cache:** compare `com-cache` vs `com-cache-rerun` (cache quente).

## Ajustes recomendados por tipo de repo

| Repo | RAG | Sugestão |
|------|-----|----------|
| Katas flat (code-katas) | Fraco | `RAG_SKIP_ISOLATED_SYMBOLS=true`, perfil `sem-rag` ou `rag-limitado` |
| Biblioteca (PyJWT) | Forte | `rag-completo`, `RETRIEVER_TOP_K_FUNCTIONS=3`, 2ª passagem cache |
| Monorepo grande | Médio | Aumentar `RETRIEVER_SCORE_THRESHOLD` para 0.6–0.65 |

## Próximas melhorias (roadmap)

1. **Warm-start de testes** — indexar `tests/` do repo alvo (opt-in) antes da geração.
2. **RAG no reparo** — enviar trecho RAG mínimo também ao `RepairAgent`.
3. **Telemetria RAG** — contar skips/filtros em `suite_metrics.json`.
4. **Perfil auto** — escolher `sem-rag` vs `rag-completo` pela densidade do grafo de chamadas.

## Variáveis `.env` (resumo)

| Variável | Padrão | Efeito |
|----------|--------|--------|
| `RAG_SKIP_ISOLATED_SYMBOLS` | `true` | Pula RAG em símbolos triviais |
| `RAG_MIN_BRANCHES_FOR_ENRICHMENT` | `1` | Limiar de branches para gating |
| `RAG_MIN_HYBRID_SCORE` | `0.35` | Filtra related fracos |
| `RAG_SAME_MODULE_BOOST` | `0.15` | Prioriza mesmo diretório |
| `RETRIEVER_SCORE_THRESHOLD` | `0.55` | Similaridade mínima (símbolos) |
| `RETRIEVER_TEST_SCORE_THRESHOLD` | `0.45` | Similaridade mínima (testes) |
| `PROMPT_MAX_RAG_TOTAL_CHARS` | `2500` | Orçamento do bloco RAG |
| `RETRIEVER_TOP_K_FUNCTIONS` | `2` | Top related após rerank |

Ver também: [CONFIGURATION.md](CONFIGURATION.md), [ARCHITECTURE.md](ARCHITECTURE.md).
