# Prompts e técnicas

Referência das instruções enviadas ao LLM e das técnicas de enriquecimento, controle e pós-processamento usadas no pipeline de geração de testes.

## Visão geral

O pipeline usa **dois system prompts** (geração e reparo) e **um user prompt estruturado** montado a partir de `FunctionContext`. O contexto RAG é injetado no user prompt em seções priorizadas, com deduplicação e orçamento de caracteres.

```
prompts/templates/generator_system.txt  →  TestGeneratorAgent  (temperature=0.1)
FunctionContext.to_prompt_block()       →  user prompt de geração

prompts/templates/repair_system.txt     →  RepairAgent         (temperature=0.1)
_build_repair_prompt()                  →  user prompt de reparo (compact=True)
```

Arquivos principais:

| Arquivo | Papel |
|---|---|
| `prompts/templates/generator_system.txt` | Instruções fixas de geração |
| `prompts/templates/repair_system.txt` | Instruções fixas de reparo |
| `prompts/loader.py` | Carrega templates e interpola limites |
| `prompts/rag.py` | Dedup, truncamento e orçamento do bloco RAG |
| `prompts/rag_headers.yaml` | Cabeçalhos das seções RAG |
| `schemas/context.py` | Montagem do user prompt (`to_prompt_block`) |

Versões registradas no código: `PROMPT_VERSION = "2"`, `GENERATOR_VERSION = "1"`.

---

## System prompt — geração

**Arquivo:** `prompts/templates/generator_system.txt`  
**Carregado por:** `build_generator_system_prompt(max_test_functions, max_lines)`  
**Parâmetros interpolados:** `{max_fn}` e `{max_lines}` vêm de `GENERATION_MAX_TEST_FUNCTIONS` (padrão 4) e `GENERATION_MAX_LINES` (padrão 400).

### Texto completo

```
Você gera testes pytest para um único símbolo Python.

SAÍDA:
- Retorne somente código Python executável.
- Sem markdown, cercas de código (```) ou explicações fora do código.
- Comece com imports; nada antes ou depois do código.
- Seja conciso: o menor conjunto que ainda cubra o essencial.

COMENTÁRIOS (obrigatório):
- Antes de cada função test_* (ou do @pytest.mark.parametrize quando usado), inclua um comentário # curto.
- O comentário deve dizer o que o teste verifica e qual caso/cenário cobre
  (ex.: happy path, exceção listada, branch, caso de borda).
- Prefira comentários # em vez de docstrings.

IMPORTS:
- Use o campo "módulo:" do contexto como caminho de importação.
- Importe apenas o que o teste usa; não invente módulos ou símbolos.

CONTEXTO RAG (quando presente no prompt):
- Priorize callees/callers/deps sobre funções semanticamente "parecidas".
- Testes similares servem só como referência de estilo — não copie imports deles.
- Não importe símbolos de snippets RAG; teste apenas o alvo indicado em "Função alvo".
- Se o snippet RAG for de outro módulo, ignore-o para imports e fixtures.

COBERTURA (priorize nesta ordem se o limite apertar):
1. Caminho principal (happy path).
2. Exceções explicitamente listadas em "Exceções relevantes" → pytest.raises().
3. Branches relevantes (use "Complexidade" como guia).
4. Casos de borda claramente inferíveis do contexto.
- Prefira pytest.mark.parametrize para cenários equivalentes.
- Para métodos (quando "classe:" estiver presente), instancie a classe.
- Se "Casos de borda detectados" mencionar @dataclass ou campos do construtor, passe valores para todos os campos obrigatórios ao instanciar (ex.: Calculadora(nome="x")).
- Use unittest.mock.patch só para I/O externo ou dependências realmente externas.
- Não invente APIs, atributos, exceções ou fixtures ausentes no contexto.
- Se o limite não couber tudo, mantenha testes válidos e essenciais.

LIMITES (obrigatório):
- No máximo {max_fn} funções test_*.
- No máximo {max_lines} linhas no arquivo.
```

### Técnicas embutidas no prompt de geração

| Técnica | Objetivo |
|---|---|
| Saída estruturada (só Python) | Evita parsing frágil; reforçado por `parsers/llm/response.py` |
| Comentários `#` obrigatórios | Rastreabilidade de cobertura (`extract_coverage_hints`) |
| Priorização de cobertura | Happy path → exceções → branches → bordas |
| Regras anti-alucinação | Não inventar APIs, imports ou fixtures |
| Hierarquia RAG explícita | Grafo estrutural > similaridade vetorial |
| Limites hard no prompt | Controle de custo e tamanho da resposta |

---

## User prompt — geração

**Montado por:** `FunctionContext.to_prompt_block(compact=False)`  
**Enviado por:** `TestGeneratorAgent.generate()`

### Estrutura das seções

As seções abaixo são concatenadas em ordem. Seções vazias são omitidas.

| Seção | Fonte | Conteúdo |
|---|---|---|
| `## Função alvo` | Símbolo | `nome`, `tipo`, `arquivo`, `módulo`, `classe` |
| `docstring:` | AST | Docstring do símbolo |
| `## Código-fonte` | AST | Código em bloco ` ```python ` |
| `## Imports disponíveis no arquivo` | Coletor AST | Lista de imports do arquivo |
| `## Dependências chamadas` | Coletor AST | Funções/métodos invocados pelo alvo |
| `## Exceções relevantes` | Coletor AST | Exceções lançadas/capturadas |
| `## Casos de borda detectados` | Heurísticas estáticas | Dicas de instanciação, `@dataclass`, etc. |
| `## Complexidade` | Coletor AST | Número de branches |
| Seções RAG | Retriever + `prompts/rag.py` | Ver [Bloco RAG](#bloco-rag-no-prompt) |
| `## Lacunas de cobertura` | CoverageAnalyzer | Linhas não cobertas (rodadas extras) |
| `## Cobertura atual` | CoverageAnalyzer | Percentual e branches não cobertos |

### Exemplo simplificado

```
## Função alvo
nome: calc.divide
tipo: method
arquivo: src/calc.py
módulo: calc

## Código-fonte
```python
def divide(self, a, b):
    ...
```

## Imports disponíveis no arquivo
  - from typing import ...

## Exceções relevantes
  - ZeroDivisionError

## Dependências estruturais (dependency graph)
  - symbol: calc.validate
    code:
    ...
```

---

## System prompt — reparo

**Arquivo:** `prompts/templates/repair_system.txt`  
**Carregado por:** `load_repair_system_prompt()`

### Texto completo

```
Você é um engenheiro de testes Python especialista. Um arquivo de teste pytest gerado falhou.

Sua tarefa: corrigir o código que falhou para que TODOS os testes passem.

FORMATO DE SAÍDA:
- APENAS código-fonte Python puro.
- NÃO envolva a saída em blocos de código markdown (sem ``` ou ```python).
- Comece diretamente com as instruções de import.
- Nenhum texto ou prosa antes ou depois do código.

ESTRATÉGIA DE REPARO:
1. Leia a saída de erro com atenção para entender a causa raiz.
2. Problemas comuns e correções:
   - ImportError / ModuleNotFoundError → corrija o caminho de importação usando o 
     campo "arquivo:" no contexto (ex: "src/calc.py" → "from calc import …")
   - TypeError (argumentos incorretos) → corrija a chamada para corresponder à assinatura real
   - AssertionError → corrija o valor esperado para corresponder ao comportamento real
   - AttributeError → o nome da classe/função pode estar errado; verifique o contexto
   - NameError → adicione o import ausente ou corrija o identificador
3. Mantenha todos os testes que já estavam corretos.
4. NÃO remova casos de teste — em vez disso, corrija-os.
5. NÃO altere o que está sendo testado; apenas corrija como é chamado ou verificado (assert).
```

### User prompt — reparo

**Montado por:** `_build_repair_prompt()` em `agents/repair.py`

1. `# Tentativa de reparo {attempt}`
2. `## Função sob teste` — `ctx.to_prompt_block(compact=True)`
3. `## Arquivo de teste falho` — código em ` ```python `
4. `## Saída de erro do pytest` — truncada em `REPAIR_ERROR_MAX_CHARS` (padrão 900)
5. Instrução final: *"Gere apenas o arquivo de teste Python corrigido."*

### Modo compacto (`compact=True`)

No reparo, o contexto é reduzido:

- **Omite:** seções RAG completas, `## Dependências chamadas`, metadados extras de cobertura.
- **Inclui:** imports do arquivo, código-fonte, exceções, bordas, complexidade.
- **Inclui parcialmente:** até 2 snippets (200 chars cada) de callees/callers em `## Contexto estrutural (reparo)`.

---

## Bloco RAG no prompt

### Categorias e prioridade

Definidas em `prompts/rag.py` (`RagCategory`). Valor menor = maior prioridade. Em caso de estouro de orçamento, itens de **menor prioridade** são removidos primeiro.

| Ordem | Categoria | Cabeçalho (`rag_headers.yaml`) | Origem |
|---|---|---|---|
| 1 | `DEPENDENCY` | Dependências estruturais (dependency graph) | Dependency graph |
| 2 | `CALLEE` | Funções chamadas (call graph) | Call graph |
| 3 | `CALLER` | Funções chamadoras (call graph) | Call graph |
| 4 | `RELATED` | Funções relacionadas (busca híbrida) | Qdrant + rerank |
| 5 | `SIMILAR_TEST` | Testes similares existentes | Coleção `tests` no Qdrant |

### Técnicas de montagem (`prompts/rag.py`)

| Técnica | Função | Descrição |
|---|---|---|
| **Deduplicação** | `deduplicate_rag_items()` | Chave por `stable_id`, `qualified_name` ou hash do código; mantém a ocorrência de maior prioridade |
| **Compactação** | `compact_rag_snippet()` | Extrai só o corpo `code:`; remove metadados `symbol:` quando possível |
| **Truncamento UTF-8 seguro** | `truncate_utf8()` | Trunca por code points, nunca parte caractere multibyte |
| **Orçamento global** | `build_rag_prompt_sections()` | Limite `PROMPT_MAX_RAG_TOTAL_CHARS` (padrão 2500) no **corpo** das bullets; cabeçalhos ficam fora |
| **Orçamento por snippet** | idem | `PROMPT_MAX_RAG_SNIPPET_CHARS` (padrão 300) por item |
| **Telemetria** | `RagPromptMetrics` | Loga candidatos, dedup, chars antes/depois, itens descartados |

---

## Técnicas de recuperação (RAG)

Implementadas em `retrieval/retriever.py`, `retrieval/hybrid.py` e `retrieval/rag_policy.py`.

### 1. Busca híbrida

Combina três sinais + bônus de módulo:

```
score = 0.5 × similaridade_vetorial
      + 0.3 × dependency_score
      + 0.2 × call_graph_score
      + 0.15 × same_module_score   (se mesmo diretório)
```

Pesos configuráveis via `RETRIEVER_*_WEIGHT` e `RAG_SAME_MODULE_BOOST`.

Fluxo:

1. Embedding da consulta (mesmo formato de `to_embedding_doc()` usado na indexação).
2. ANN no Qdrant (`RETRIEVER_RERANK_POOL_SIZE` candidatos, padrão 10).
3. Enriquecimento com vizinhos de call graph e dependency graph.
4. Rerank com `rerank_candidates()` → top `RETRIEVER_TOP_K_FUNCTIONS` (padrão 3).
5. Busca separada na coleção `tests` com limiar `RETRIEVER_TEST_SCORE_THRESHOLD` (0.45).

### 2. Gating de símbolos triviais

`should_apply_rag()` pula RAG quando `RAG_SKIP_ISOLATED_SYMBOLS=true` (padrão) e o símbolo é:

- Sem callers, callees ou deps de grafo;
- Com `branches ≤ RAG_MIN_BRANCHES_FOR_ENRICHMENT` (padrão 1);
- Sem exceções, sem dependências AST, sem classe.

### 3. Filtro de score híbrido

`filter_hybrid_candidates()`:

- Vizinhos de grafo/deps **sempre passam**;
- Candidatos só vetoriais exigem `hybrid_score ≥ RAG_MIN_HYBRID_SCORE` (padrão 0.35).

### 4. Dedup entre seções

`exclude_graph_from_related()` remove de `related_functions` símbolos já presentes como callee/caller/dependency.

### 5. Boost mesmo módulo

`same_module()` dá bônus a símbolos no mesmo diretório do alvo — reduz ruído cross-pacote em repos flat (ex.: code-katas).

### 6. Documento de embedding

`to_embedding_doc()` serializa metadados + código para indexação:

```
symbol: Module.func
type: function
file: path/to/file.py
...
code:
<fonte>
```

Garante que vetores de consulta e indexados estejam no mesmo espaço semântico.

---

## Técnicas de análise estática (pré-LLM)

Extraídas na ingestão e enviadas no user prompt **sem** depender do RAG.

| Técnica | Módulo | Uso no prompt |
|---|---|---|
| AST parsing | `parsers/source/` | Código, assinatura, docstring |
| Call graph | `call_graph.py` | Callees/callers no RAG |
| Dependency graph | `dependency_graph.py` | Deps estruturais no RAG |
| Coleta de exceções | collectors | Seção `Exceções relevantes` |
| Contagem de branches | collectors | Seção `Complexidade` |
| Heurísticas de borda | edge cases | `@dataclass`, construtor, etc. |
| Resolução de módulo | `import_resolver.py` | Campo `módulo:` para imports corretos |

---

## Técnicas pós-LLM

### Parsing da resposta (`parsers/llm/response.py`)

| Etapa | Técnica |
|---|---|
| `normalize_code_response()` | Remove BOM, cercas markdown, detecta truncamento |
| `validate_syntax()` | `ast.parse()` — rejeita código inválido |
| `warn_generation_limits()` | Alerta se excede `GENERATION_MAX_*` |
| `normalize_test_imports()` | Corrige caminhos de import com base em `module_name` |
| `extract_coverage_hints()` | Extrai comentários `#` acima de cada `test_*` |

### Reparo iterativo

- Até `MAX_REPAIRS` tentativas (padrão 1) por símbolo.
- Cada tentativa envia erro truncado + contexto compacto.
- Temperatura 0.1 (determinismo).

### Loop de cobertura (opcional)

Quando `MAX_COVERAGE_ROUNDS > 0`:

1. `CoverageAnalyzer` mede cobertura da função alvo.
2. Se abaixo de `COVERAGE_THRESHOLD` (80%), injeta lacunas em `FunctionContext`.
3. Regenera teste com seções `## Lacunas de cobertura` e `## Branches não cobertos`.
4. Para se `COVERAGE_STOP_ON_NO_IMPROVEMENT=true` e percentual estagnar.

### Cache de geração

Com `GENERATION_CACHE_ENABLED=true` (perfil `com-cache`):

- Consulta cache antes de chamar o LLM.
- Chave baseada em contexto + versão do prompt/gerador.
- Hit não consome orçamento `MAX_LLM_CALLS_PER_SYMBOL`.

---

## Perfis e orçamentos

Os perfis (`config/run_profiles.py`) alteram quanto RAG entra no prompt:

| Perfil | `RAG_MODE` | Orçamento RAG |
|---|---|---|
| `sem-rag` | `none` | Nenhum (indexação e retriever pulados) |
| `rag-limitado` | `limited` | `PROMPT_MAX_RAG_TOTAL_CHARS=600`, `RETRIEVER_TOP_K_FUNCTIONS=1`, snippet 150 chars |
| `rag-completo` | `full` | Padrões do `.env` (2500 / 300) |
| `com-cache` | `full` | Igual `rag-completo` + cache |

---

## Parâmetros relevantes

| Variável | Padrão | Efeito no prompt |
|---|---|---|
| `GENERATION_MAX_TEST_FUNCTIONS` | 4 | `{max_fn}` no system prompt |
| `GENERATION_MAX_LINES` | 400 | `{max_lines}` no system prompt |
| `PROMPT_MAX_RAG_TOTAL_CHARS` | 2500 | Orçamento do corpo RAG |
| `PROMPT_MAX_RAG_SNIPPET_CHARS` | 300 | Tamanho máximo por snippet |
| `REPAIR_ERROR_MAX_CHARS` | 900 | Truncamento do stderr do pytest |
| `RETRIEVER_TOP_K_FUNCTIONS` | 3 | Quantidade de `related` após rerank |
| `RETRIEVER_TOP_K_TESTS` | 2 | Testes similares no prompt |
| `RAG_SKIP_ISOLATED_SYMBOLS` | `true` | Omite bloco RAG inteiro em símbolos triviais |

Lista completa: [CONFIGURATION.md](CONFIGURATION.md). Ajuste fino do RAG: [RAG_TUNING.md](RAG_TUNING.md).

---

## Como editar prompts

1. **System prompts:** edite `prompts/templates/*.txt` — não requer alteração de código.
2. **Cabeçalhos RAG:** edite `prompts/rag_headers.yaml`.
3. **Estrutura do user prompt:** edite `FunctionContext.to_prompt_block()` em `schemas/context.py`.
4. **Orçamento/prioridade RAG:** edite `prompts/rag.py` ou variáveis `PROMPT_MAX_RAG_*`.
5. **Regras de recuperação:** edite `retrieval/rag_policy.py` e pesos em `.env`.

Após mudanças nos templates, incremente `PROMPT_VERSION` em `agents/test_generator.py` se o cache de geração estiver ativo.

---

## Referências cruzadas

- [ARCHITECTURE.md](ARCHITECTURE.md) — fases do pipeline e diagrama
- [RAG_TUNING.md](RAG_TUNING.md) — problemas observados e protocolo de avaliação
- [CLI.md](CLI.md) — perfis `--profile`
- [API.md](API.md) — uso programático de `TestGeneratorAgent` e `RepairAgent`
