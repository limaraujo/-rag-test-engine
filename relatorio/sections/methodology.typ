#let methodology = [
  = Metodologia
  Esta seção detalha o planejamento experimental, a arquitetura do pipeline, os critérios de avaliação e os protocolos comparativos utilizados para mensurar o impacto do RAG na geração autônoma de testes unitários.

  == Objetivo e Questões de Pesquisa

  Para guiar o experimento, foram definidas as seguintes Questões de Pesquisa:

  - QP1: Qual é o impacto do RAG híbrido (vetorial + grafos) na taxa de sucesso dos testes gerados em comparação a um baseline sem contexto recuperado?
  - QP2: O contexto estruturado recuperado dinamicamente reduz o número de iterações necessárias no ciclo de reparo autônomo?
  - QP3: Como a arquitetura proposta afeta a cobertura de código (linhas e branches) nas suítes analisadas?
  - QP4: Qual é o trade-off entre qualidade (taxa de sucesso, cobertura) e custo computacional (tokens gastos)?

  == Arquitetura do Pipeline

  A solução propõe um pipeline de 8 fases orquestradas que transforma um repositório de código em uma suíte de testes pytest automaticamente gerada:

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

  == Seleção da Amostra e Dados

  O experimento é executado em repositórios Python open-source consolidados (não fragmentos isolados de código), garantindo cenários realistas com dependências inter-módulos, classes aninhadas e lógica complexa. Repositório 1: PyJWT e o Repositório 2: Code Katas. A amostra inclui símbolos selecionados por critérios estruturais: exclusão de métodos triviais, priorização de métodos com complexidade moderada a alta. O volume de testes gerados é suficiente para análise estatística robusta.

  == Métricas de Avaliação

  === Taxa de Sucesso (Pass Rate - PR)
  Proporção de testes que compilam, executam sem erros e passam em todas as asserções (após execução inicial ou reparo bem-sucedido).

  $ "PR" = ("T_pass" / "T_total") * 100 $

  === Cobertura de Código (Code Coverage - CC)
  Percentual de linhas e branches do código original que foram exercitadas pelo teste.

  $ "CC" = ("L_exec" / "L_total") * 100 $

  === Autonomia / Esforço de Reparo (Repair Effort - RE)
  Média de iterações do ciclo de reparo necessárias para aprovação ou descarte.

  $ "RE" = (1 / N) sum_(i=1)^N I_i $

  == Experimento

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