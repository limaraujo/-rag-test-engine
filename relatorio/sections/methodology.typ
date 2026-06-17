#let methodology = [
  = Metodologia
  Esta seção detalha o planejamento experimental, a arquitetura do pipeline, os critérios de avaliação e os protocolos comparativos utilizados para mensurar o impacto do RAG na geração autônoma de testes unitários.

  == Objetivo e Questões de Pesquisa

  Para guiar o experimento, foram definidas as seguintes Questões de Pesquisa:

  - QP1: Qual é o impacto do RAG híbrido (vetorial + grafos) na taxa de sucesso dos testes gerados em comparação a um baseline sem contexto recuperado?
  - QP2: O contexto estruturado recuperado dinamicamente reduz o número de iterações necessárias no ciclo de reparo autônomo?
  - QP3: Como a arquitetura proposta afeta a cobertura de código (linhas e branches) nas suítes analisadas?

  == Arquitetura do Pipeline

  A solução propõe um pipeline de 8 fases orquestradas pelo `OrchestratorAgent` que transforma um repositório de código em uma suíte de testes pytest automaticamente gerada. O diferencial metodológico é a transformação do repositório em um banco vetorial antes da geração do código, permitindo que o LLM consulte dependências externas em tempo real.

  === Fase 1: Ingestão e Estruturação
  O repositório é analisado via Abstract Syntax Tree (AST) para extrair símbolos estruturados (funções, métodos, classes). O sistema constrói dois grafos: (1) grafo de chamadas (caller-callee) que mapeia quem chama quem; (2) grafo de dependências que captura importações inter-módulos. Símbolos triviais (getters, setters, `__init__` simples) e classes encapsuladores são filtrados. Todos os símbolos brutos, grafos e estatísticas de seleção são persistidos para rastreabilidade.

  === Fase 2: Indexação Vetorial
  Cada símbolo elegível é transformado em um documento textual (nome, assinatura, corpo, docstring, imports) e convertido em embedding de alta dimensionalidade via modelo de embeddings. Os embeddings são persistidos em um banco de dados vetorial (Qdrant) para rápida recuperação posterior.

  === Fase 3: Enriquecimento de Contexto (Busca Híbrida)
  Para cada símbolo alvo, o sistema recupera contexto relevante através de três canais simultâneos: (1) busca de similaridade vetorial no banco de dados (código semelhante); (2) análise do grafo de chamadas (funções que chamam ou são chamadas); (3) análise do grafo de dependências (classes/funções importadas). Os resultados são combinados via score ponderado e filtrados para manter apenas os mais relevantes dentro de um orçamento de tokens configurável.

  === Fase 4: Geração de Testes
  O contexto recuperado é integrado com a assinatura e corpo do método alvo em um prompt formatado. O LLM recebe o método isolado (baseline) ou enriquecido com contexto (com RAG) dependendo do perfil de teste. O LLM gera código pytest candidato. Opcionalmente, o sistema consulta um cache de testes já aprovados antes de chamar o LLM, economizando chamadas de API.

  === Fase 5: Execução e Validação
  O código gerado é executado via pytest em um ambiente isolado. O sistema captura o status de execução (passou/falhou) e mede a cobertura de código (percentual de linhas e branches exercitadas).

  === Fase 6: Reparo Autônomo
  Se o teste falha, o sistema injeta a mensagem de erro (stack trace, assertion failures) em um novo prompt e pede ao LLM que corrija o código. Este ciclo se repete até que o teste passe ou um limite de iterações seja atingido. O objetivo é resolver erros comuns (imports inválidos, ausência de mocks) sem regeneração completa.

  === Fase 7: Otimização de Cobertura
  Se o teste passou mas cobriu menos do que um threshold configurado (definimos como 80%), o sistema identifica as linhas/branches não cobertos e injeta essa informação como "dica" em um novo prompt para o LLM. O teste é regenerado buscando aumentar cobertura. Este passo é opcional, podendo ser alterado a cada execução.

  === Fase 8: Salvamento e Validação de Suíte
  Todos os testes aprovados são salvos em arquivos. Ao final, a suíte completa é re-executada para medir cobertura agregada e confirmar que todos os testes funcionam em conjunto. Metadados finais (tokens gastos, número de iterações, estatísticas) são compilados.

  == Prompt do Gerador
  O system prompt enviado ao LLM na fase de geração é carregado de `prompts/templates/generator_system.txt` pela função `build_generator_system_prompt(max_fn, max_lines)`. Seus parâmetros `{max_fn}` e `{max_lines}` são interpolados via variáveis de ambiente (`GENERATION_MAX_TEST_FUNCTIONS=4`, `GENERATION_MAX_LINES=400`). O texto completo é reproduzido abaixo:

  #block(
    fill: luma(240),
    inset: 8pt,
    radius: 4pt,
    [
      #set text(size: 8pt)
      Você gera testes pytest para um único símbolo Python.

      SAÍDA:\
      - Retorne somente código Python executável.\
      - Sem markdown, cercas de código (\`\`\`) ou explicações fora do código.\
      - Comece com imports; nada antes ou depois do código.\
      - Seja conciso: o menor conjunto que ainda cubra o essencial.

      COMENTÁRIOS (obrigatório):\
      - Antes de cada função test\_\* (ou do \@pytest.mark.parametrize quando usado), inclua um comentário \# curto.\
      - O comentário deve dizer o que o teste verifica e qual caso/cenário cobre (ex.: happy path, exceção listada, branch, caso de borda).\
      - Prefira comentários \# em vez de docstrings.

      IMPORTS:\
      - Use o campo "módulo:" do contexto como caminho de importação.\
      - Importe apenas o que o teste usa; não invente módulos ou símbolos.

      CONTEXTO RAG (quando presente no prompt):\
      - Priorize callees/callers/deps sobre funções semanticamente "parecidas".\
      - Testes similares servem só como referência de estilo — não copie imports deles.\
      - Não importe símbolos de snippets RAG; teste apenas o alvo indicado em "Função alvo".\
      - Se o snippet RAG for de outro módulo, ignore-o para imports e fixtures.

      COBERTURA (priorize nesta ordem se o limite apertar):\
      1. Caminho principal (happy path).\
      2. Exceções explicitamente listadas em "Exceções relevantes" → pytest.raises().\
      3. Branches relevantes (use "Complexidade" como guia).\
      4. Casos de borda claramente inferíveis do contexto.\
      - Prefira pytest.mark.parametrize para cenários equivalentes.\
      - Para métodos (quando "classe:" estiver presente), instancie a classe.\
      - Use unittest.mock.patch só para I/O externo ou dependências realmente externas.\
      - Não invente APIs, atributos, exceções ou fixtures ausentes no contexto.\
      - Se o limite não couber tudo, mantenha testes válidos e essenciais.

      LIMITES (obrigatório):\
      - No máximo \{max\_fn\} funções test\_\*.\
      - No máximo \{max\_lines\} linhas no arquivo.
    ]
  )

  O user prompt é montado por `FunctionContext.to_prompt_block()` e concatena as seguintes seções (omitindo as vazias): código-fonte do símbolo alvo, imports disponíveis no arquivo, dependências chamadas, exceções relevantes, casos de borda detectados estaticamente, complexidade (número de branches) e, quando RAG está ativo, os snippets de contexto recuperados pelo Retriever.

  == Técnicas de Teste Empregadas

  A análise dos testes gerados pelo sistema revela o uso consistente das seguintes técnicas:

  #figure(
    table(
      columns: (1.4fr, 2fr),
      align: (left, left),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Técnica*], [*Descrição*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Happy path],         [Cenário com entradas válidas verificando comportamento esperado],
      [Exception path],     [Verificação de exceções corretas via `pytest.raises`],
      [Edge cases],         [Valores limite, entradas vazias, tipos inválidos],
      [Parametrize],        [`@pytest.mark.parametrize` para múltiplas entradas equivalentes],
      [Mocking],            [`monkeypatch` e `unittest.mock` para isolar dependências externas],
      [Branch coverage],    [Testes separados para cada ramo condicional relevante],
      [Integração leve],    [Verificação da cadeia de chamadas internas via mocks],
      table.hline(y: 8, stroke: 0.5pt),
    ),
    caption: [Técnicas de teste utilizadas na geração automática.],
  )

  == Seleção da Amostra e Dados

  Para garantir a validade externa do experimento, o sistema foi executado em repositórios Python open-source consolidados (não fragmentos isolados de código), garantindo cenários realistas com dependências inter-módulos, classes aninhadas e lógica complexa, essenciais para testar o limite da janela de contexto do LLM. O experimento utilizou um conjunto de 184 métodos alvo, extraídos de 2 repositórios distintos, gerando um volume de testes suficiente para análise estatística. Repositório 1: PyJWT e o Repositório 2: Code Katas. A amostra foi gerada através do módulo `parser.py`, inclui símbolos selecionados por critérios estruturais: exclusão de métodos triviais, priorização de métodos com complexidade moderada a alta.

  == Métricas de Avaliação
    As métricas foram selecionadas para avaliar tanto a qualidade do produto gerado quanto o esforço computacional da ferramenta. Os resultados extraídos pelo `main.py` serão submetidos às seguintes equações:

  === Taxa de Sucesso (Pass Rate - PR)
  Mede a proporção de testes que compilam e passam com sucesso na primeira asserção válida, sem gerar erros de sintaxe ou importação. Observa-se a capacidade do modelo de gerar código pronto para uso.

  $ "PR" = ("T_pass" / "T_total") times 100 $ <eq:taxa-de-sucesso>

  Onde $T_"pass"$ é o número de testes aprovados e $T_"total"$ é o total de métodos avaliados na amostra.

  === Cobertura de Código (Code Coverage - CC)
  Indicador primário da qualidade funcional. Avalia o percentual de linhas do código original que foram efetivamente exercitadas pelo teste gerado. A cobertura é calculada exclusivamente sobre os símbolos selecionados (funções e métodos), excluindo classes.

  $ "CC" = ("L_exec" / "L_total") times 100 $ <eq:cobertura-de-codigo>

  Onde $L_"exec"$ representa as linhas de código executadas durante o teste e $L_"total"$ é o número total de linhas do método alvo.

  === Esforço de Reparo (Repair Effort - RE)
  Mede o custo computacional do ciclo de tuning. Representa a média de iterações que o módulo `repair.py` precisou executar até aprovar o código. Uma métrica menor indica maior resiliência e precisão no prompt inicial.

  $ "RE" = 1/N sum_(i=1)^N I_i $ <eq:esforco-de-reparo>

  Onde $N$ é o total de métodos e $I_i$ é o número de iterações gastas no método $i$.

  == Abordagem de Coleta de Dados

  O experimento executa o pipeline sob quatro perfis comparativos, cada um com a mesma amostra de símbolos:

  Perfil 1 - Baseline (sem RAG): O LLM recebe apenas a assinatura e corpo do método, sem contexto recuperado. Este perfil mede a linha de base de qualidade.

  Perfil 2 - RAG Limitado: Recuperação com orçamento reduzido de tokens. Simula contexto restrito para ambientes com custo apertado.

  Perfil 3 - RAG Completo: Recuperação com orçamento padrão de tokens. O LLM tem acesso a mais contexto, mas sem reutilizar testes já aprovados.

  Perfil 4 - Com Cache: Reutiliza testes já aprovados de execuções anteriores, economizando chamadas ao LLM.

  Todos os perfis compartilham a mesma ingestão (símbolos candidatos são determinísticos). Cada perfil cria um workspace isolado para rastreabilidade. Ao final, as métricas são comparadas por símbolo para isolar o efeito do RAG, cache e configurações de orçamento.

  Para garantir comparação equiparável: 
  - ingestão é única e compartilhada; 
  - cada perfil executa independentemente;
  -  métricas são cruzadas por símbolo entre perfis, controlando variáveis de confusão (ex.: mesmos símbolos em sem-rag vs rag-completo têm mesma dificuldade base).
]