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

| Repositório | Caminho correto |
|---|---|
| code-katas | `repositorios/code_katas/src` |
| Projeto flat (só `.py` na raiz) | `repositorios/meu_projeto` |
| Monorepo | `repositorios/meu_projeto/packages/api` |

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
```

Com **uv**:

```bash
uv run python main.py repositorios/code_katas/src --profile sem-rag
```

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

## 5. Comparar os quatro modos de uma vez

```bash
python scripts/run_all_profiles.py repositorios/code_katas/src
```

Cria um `run_group` compartilhado:

```
runs/repositorios_code_katas_src/20260615_143022/
├── sem-rag/logs/pipeline.log
├── rag-limitado/logs/pipeline.log
├── rag-completo/logs/pipeline.log
└── com-cache/logs/pipeline.log
```

Compare `artifacts/run_summary.json` e `token_usage` entre as pastas.

---

## 6. O que inspecionar depois

| Arquivo | Uso |
|---|---|
| `logs/pipeline.log` | Fluxo completo; seleção de arquivos/símbolos; erros por símbolo |
| `artifacts/ingest_selection.json` | Lista exata do que entrou/saiu na ingestão |
| `artifacts/run_summary.json` | Stats finais, tokens, validação pytest |
| `tests/` | Arquivos `test_*.py` gerados que passaram |
| `logs/api_calls/` | Detalhe por chamada LLM (se `LOG_API_CALLS=true`) |

Validar testes gerados manualmente:

```bash
python -m pytest runs/repositorios_code_katas_src/sem-rag/<timestamp>/tests -v
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

# 3. Pipeline sem RAG
python main.py repositorios/code_katas/src --profile sem-rag

# 4. (Opcional) Comparar os 4 perfis
python scripts/run_all_profiles.py repositorios/code_katas/src
```

---

## Referências

- [CLI.md](CLI.md) — argumentos e layout de `runs/`
- [CONFIGURATION.md](CONFIGURATION.md) — `.env`, exclusões de ingestão, tokens
- [ARCHITECTURE.md](ARCHITECTURE.md) — fases do pipeline
- [API.md](API.md) — uso programático (`main()`, `run_ingest()`)
