# Testar um repositório externo

Guia passo a passo para clonar um projeto Python, apontar o RAG Test Engine para ele e rodar nos quatro modos de teste.

## Pré-requisitos

1. **Engine instalado** — venv ativo, dependências do `requirements.txt`.
2. **`.env` configurado** — copie de `.env.example`; no mínimo `OPENAI_API_KEY`.
3. **Qdrant** (perfis com RAG) — servidor em `http://localhost:6333` ou ajuste `QDRANT_URL`.
4. **Git** — para clonar repositórios.

Modo `sem-rag` **não exige** Qdrant nem embeddings. Os demais perfis usam indexação vetorial.

Ver também: [CONFIGURATION.md](CONFIGURATION.md), [CLI.md](CLI.md#perfis-de-teste---profile).

---

## 1. Pasta `repositorios/`

Na raiz do engine, use uma pasta fixa para clones (não versionada por padrão):

```
-rag-test-engine/
├── repositorios/          ← clones aqui
│   └── code_katas/
│       ├── src/           ← aponte o pipeline para cá
│       └── README.md
├── main.py
└── ...
```

**Por que `repositorios/`?**

- Mantém o código alvo separado do engine.
- O slug em `runs/` deriva do caminho relativo (`repositorios/code_katas/src` → `repositorios_code_katas_src`).

**Nome do clone:** prefira **underscore** em vez de hífen (`code_katas`, não `code-katas`). Hífen quebra imports Python gerados (`repositorios.code-katas` é inválido).

---

## 2. Clonar o repositório

Exemplo com [code-katas](https://github.com/rwisecar/code-katas):

```bash
cd /caminho/para/-rag-test-engine

mkdir -p repositorios
git clone https://github.com/rwisecar/code-katas.git repositorios/code_katas
```

**Windows (PowerShell):**

```powershell
cd "C:\...\ -rag-test-engine"
New-Item -ItemType Directory -Force -Path repositorios
git clone https://github.com/rwisecar/code-katas.git repositorios/code_katas
```

**WSL** (mesmo repo no `/mnt/c/...`):

```bash
cd "/mnt/c/Users/.../-rag-test-engine"
mkdir -p repositorios
git clone https://github.com/rwisecar/code-katas.git repositorios/code_katas
```

### Aponte para o código-fonte, não a raiz do clone

Muitos repos têm testes junto do código (`src/test_*.py`). O engine **ignora** `test_*.py` na ingestão, mas você deve passar a pasta onde está o **código de produção**:

| Repositório | Caminho correto | Símbolos elegíveis (approx.) |
|---|---|---|
| [code-katas](https://github.com/rwisecar/code-katas) | `repositorios/code_katas/src` | ~58 |
| [PyJWT](https://github.com/jpadilla/pyjwt) | `repositorios/pyjwt/jwt` | ~126 |
| Projeto flat (só `.py` na raiz) | `repositorios/meu_projeto` | — |
| Monorepo | `repositorios/meu_projeto/packages/api` | — |

**PyJWT:** aponte para a pasta `jwt/` (pacote Python), não a raiz do clone (que contém `tests/` do upstream). Muitos algoritmos exigem `cryptography` em runtime (`pip install cryptography`).

---

## 3. Validar só o parser (recomendado antes do LLM)

Roda ingestão **sem** OpenAI, Qdrant ou pytest de geração. Útil para ver quantos arquivos/símbolos entram antes de gastar tokens.

```bash
python scripts/ingest_only.py repositorios/code_katas/src
```

**Saída:**

```
runs/repositorios_code_katas_src/<timestamp>/
├── logs/pipeline.log
└── artifacts/
    ├── symbols.json
    ├── call_graph.json
    ├── dependency_graph.json
    └── ingest_selection.json   # incluídos vs ignorados + motivos
```

No log, procure:

```
[ingest] arquivos: 25 incluído(s), 23 ignorado(s)
  [arquivo +] even_odd.py
  [arquivo -] test_even_odd.py (glob:test_*.py)
[ingest] símbolos: 58 elegíveis para testes, 6 filtrados
  [símbolo +] make_negative (function)
  [símbolo -] Graph (class) — container_class
```

Se o parse falhar (ex.: sintaxe Python 2 legada), corrija ou exclua o arquivo antes do pipeline completo.

---

## 4. Rodar o pipeline completo por modo

Todos os comandos usam `main.py` com `--profile`. Cada perfil sobrescreve `RAG_MODE` e cache **só durante a execução**.

### Tabela de perfis

| Perfil | RAG | Cache de geração | Qdrant | Custo LLM |
|---|---|---|---|---|
| `sem-rag` | Desligado | Desligado | Não precisa | 1× geração por símbolo |
| `rag-limitado` | Enxuto (menos contexto) | Desligado | Sim | Similar, prompts menores |
| `rag-completo` | Completo (`.env`) | Desligado | Sim | Máximo contexto RAG |
| `com-cache` | Completo | Ligado | Sim | Reutiliza testes já aprovados |

### Comandos

Substitua `repositorios/code_katas/src` pelo seu caminho.

```bash
# Baseline — sem RAG, sem cache (ideal para primeiro teste com LLM)
python main.py repositorios/code_katas/src --profile sem-rag

# RAG com orçamento reduzido
python main.py repositorios/code_katas/src --profile rag-limitado

# RAG completo, sempre regenera via LLM
python main.py repositorios/code_katas/src --profile rag-completo

# RAG completo + reutiliza testes do cache persistente
python main.py repositorios/code_katas/src --profile com-cache

# Limpar cache persistente depois de cada execução (recomendado)
python scripts/clear_cache.py
```

Com **uv**:

```bash
uv run python main.py repositorios/code_katas/src --profile sem-rag
python scripts/clear_cache.py
```

### Limpar cache após rodar

O perfil `com-cache` grava testes aprovados em **`.cache/generation/`** (ou `GENERATION_CACHE_DIR`). Para comparar perfis de forma justa ou evitar reutilizar gerações antigas, **limpe o cache depois de cada run**:

```bash
python scripts/clear_cache.py
```

**PowerShell (equivalente):**

```powershell
Remove-Item -Recurse -Force .cache\generation -ErrorAction SilentlyContinue
```

| O que limpa | O que **não** limpa |
|---|---|
| `.cache/generation/` (testes aprovados em disco) | Embeddings no **Qdrant** (use `REINDEX_SYMBOLS=true` ou apague a coleção no servidor) |
| | Pastas em `runs/` (workspaces e testes gerados) |

Ver [CONFIGURATION.md](CONFIGURATION.md) (seção *Cache de geração e limpeza*).

### Layout de saída por perfil

```
runs/repositorios_code_katas_src/
├── sem-rag/
│   └── 20260614_223744/
│       ├── tests/              # testes aprovados
│       ├── logs/pipeline.log
│       └── artifacts/run_summary.json
├── rag-limitado/
│   └── ...
├── rag-completo/
│   └── ...
└── com-cache/
    └── ...
```

Sem `--profile`, a pasta fica `runs/<slug>/<timestamp>/` (sem subpasta de perfil).

---

## 5. Comparar perfis (protocolo justo)

```bash
python scripts/run_all_profiles.py repositorios/code_katas/src
```

**Protocolo `fair` (padrão)** — compara RAG e cache de forma separada:

| Passo | Perfil | Limpa cache depois? |
|-------|--------|---------------------|
| início | — | sim (cache vazio) |
| 1 | `sem-rag` | sim |
| 2 | `rag-limitado` | sim |
| 3 | `rag-completo` | sim |
| 4 | `com-cache` | **não** (popula cache) |
| 5 | `com-cache-rerun` | sim (mede hits, limpa ao final) |

- **RAG:** compare `sem-rag`, `rag-limitado`, `rag-completo` e a 1ª passagem `com-cache` (todas com cache frio entre si).
- **Cache:** compare `com-cache` (fria) vs `com-cache-rerun` (quente) — hits e tokens devem cair na 2ª.

Comportamento antigo (limpa cache após cada perfil, sem 2ª passagem):

```bash
python scripts/run_all_profiles.py repositorios/code_katas/src --protocol legacy
```

Cria um `run_group` compartilhado:

```
runs/repositorios_code_katas_src/20260615_143022/
├── sem-rag/logs/pipeline.log
├── rag-limitado/logs/pipeline.log
├── rag-completo/logs/pipeline.log
├── com-cache/logs/pipeline.log
└── com-cache-rerun/logs/pipeline.log
```

Tabela comparativa:

```bash
python scripts/compare_run_metrics.py runs/repositorios_code_katas_src/20260615_143022 \
  --md-out runs/repositorios_code_katas_src/20260615_143022/artifacts/METRICS_COMPARISON.md
```

---

## 6. O que inspecionar depois

| Arquivo | Uso |
|---|---|
| `logs/pipeline.log` | Fluxo completo; seleção de arquivos/símbolos; erros por símbolo |
| `artifacts/ingest_selection.json` | Lista exata do que entrou/saiu na ingestão |
| `artifacts/run_summary.json` | Stats finais, tokens, validação pytest, `suite_metrics` |
| `artifacts/suite_metrics.json` | Tabela de métricas da suíte (validade, cobertura, custo) |
| `tests/` | Arquivos `test_*.py` gerados que passaram |
| `logs/api_calls/` | Detalhe por chamada LLM (se `LOG_API_CALLS=true`) |

Validar testes gerados manualmente:

```bash
python -m pytest runs/repositorios_code_katas_src/sem-rag/<timestamp>/tests -v
python scripts/clear_cache.py
```

---

## 7. Checklist rápido

```
[ ] Clone em repositorios/<nome_sem_hifen>/
[ ] SOURCE_DIR aponta para pasta com código (ex.: .../src)
[ ] scripts/ingest_only.py — parse ok, símbolos esperados
[ ] .env com OPENAI_API_KEY
[ ] Qdrant rodando (se perfil ≠ sem-rag)
[ ] main.py ... --profile sem-rag (primeiro run barato)
[ ] python scripts/clear_cache.py após run isolado (lote `fair` limpa automaticamente)
[ ] Demais perfis conforme necessidade
```

---

## 8. Problemas comuns

### Slug errado ou pasta `runs/src/`

Antes, só o último segmento do path virava slug (`src`). Agora o slug usa o caminho relativo completo. Use paths como `repositorios/code_katas/src`, não só `src`.

### Muitos símbolos → muito custo

code-katas tem dezenas de símbolos elegíveis. Comece com `sem-rag` ou limite temporariamente o diretório a um subconjunto de arquivos.

### `SyntaxError: invalid non-printable character U+FEFF`

Arquivo salvo com BOM UTF-8. O engine sanitiza BOM na leitura e nas respostas LLM; remova BOM do fonte se persistir (`UTF-8` sem BOM no editor).

### Código Python 2 legado

Alguns repos antigos não parseiam em Python 3.12+. Aparecem no ingest como falha de parse — exclua ou adapte o arquivo.

### `SOURCE_DIR_STRICT=true` bloqueia

Muitos arquivos `.py` ou diretório arriscado:

```bash
python main.py repositorios/code_katas/src --allow-risky-source
```

### Imports nos testes gerados

O `PYTHONPATH` inclui a raiz do engine. Imports ficam no formato `repositorios.code_katas.src.modulo`. Por isso o clone deve ficar **dentro** do engine e sem hífen no nome da pasta.

### Qdrant indisponível (perfis com RAG)

```bash
# Docker, por exemplo
docker run -p 6333:6333 qdrant/qdrant
```

Ou use `--profile sem-rag` até o Qdrant estar no ar.

---

## 9. Exemplo completo (code-katas)

```bash
# 1. Clone
git clone https://github.com/rwisecar/code-katas.git repositorios/code_katas

# 2. Parser only
python scripts/ingest_only.py repositorios/code_katas/src

# 3. Pipeline sem RAG + limpar cache
python main.py repositorios/code_katas/src --profile sem-rag
python scripts/clear_cache.py

# 4. (Opcional) Comparar os 4 perfis — cache limpo após cada perfil por padrão
python scripts/run_all_profiles.py repositorios/code_katas/src
```

**PowerShell (fluxo recomendado):**

```powershell
cd "C:\...\ -rag-test-engine"
python scripts/ingest_only.py repositorios/code_katas/src
python main.py repositorios/code_katas/src --profile sem-rag
python scripts/clear_cache.py
# ou os 4 perfis de uma vez:
python scripts/run_all_profiles.py repositorios/code_katas/src
```

---

## 10. Exemplo completo (PyJWT)

Repositório: [jpadilla/pyjwt](https://github.com/jpadilla/pyjwt) — implementação JWT em Python.

```bash
# 1. Clone (underscore no nome da pasta)
git clone https://github.com/jpadilla/pyjwt.git repositorios/pyjwt

# 2. Parser only — slug: repositorios_pyjwt_jwt
python scripts/ingest_only.py repositorios/pyjwt/jwt

# 3. Baseline (recomendado primeiro — ~126 símbolos, custo alto)
python main.py repositorios/pyjwt/jwt --profile sem-rag
python scripts/clear_cache.py

# 4. Comparar os 4 perfis (pode levar horas)
python scripts/run_all_profiles.py repositorios/pyjwt/jwt

# 5. Tabela comparativa entre perfis
python scripts/compare_run_metrics.py runs/repositorios_pyjwt_jwt/<run_group>
```

**PowerShell:**

```powershell
cd "C:\...\ -rag-test-engine"
git clone https://github.com/jpadilla/pyjwt.git repositorios/pyjwt
python scripts/ingest_only.py repositorios/pyjwt/jwt
python main.py repositorios/pyjwt/jwt --profile sem-rag
python scripts/clear_cache.py
```

**Escala:** ~126 símbolos elegíveis (2× code-katas). Estime ~45–90 min e centenas de milhares de tokens **por perfil**. Comece sempre com `sem-rag` antes do lote dos 4.

**Saída:** `runs/repositorios_pyjwt_jwt/<run_group>/<profile>/`

---

## Referências

- [CLI.md](CLI.md) — argumentos e layout de `runs/`
- [CONFIGURATION.md](CONFIGURATION.md) — `.env`, exclusões de ingestão, tokens
- [ARCHITECTURE.md](ARCHITECTURE.md) — fases do pipeline
- [API.md](API.md) — uso programático (`main()`, `run_ingest()`)
