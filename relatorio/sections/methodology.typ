#let methodology = [
  = Metodologia
  Esta seção detalha o planejamento experimental, a arquitetura do sistema desenvolvido e os critérios de avaliação utilizados para mensurar a eficácia da integração.

  == Objetivo e Questões de Pesquisa
  O objetivo principal deste trabalho é investigar se, e em que medida, a injeção de contexto dinâmico via RAG melhora a precisão e reduz o esforço computacional de LLMs na geração autônoma de testes unitários. Para guiar o experimento, foram definidas as seguintes Questões de Pesquisa:

  - QP1: Qual é o impacto da utilização do RAG na taxa de sucesso dos testes gerados em comparação a um modelo de contexto estático?
  - QP2: A provisão de contexto estruturado reduz o número de iterações necessárias no ciclo autônomo de correção?
  - QP3: Como a arquitetura proposta afeta a métrica final de cobertura de código nas amostras analisadas?

  == Arquitetura do Sistema
  A solução proposta consiste em um pipeline automatizado desenvolvido em Python que orquestra modelos de LLM. O diferencial metodológico é a transformação do repositório em um banco vetorial antes da geração do código, permitindo que o LLM consulte dependências externas em tempo real. A execução é coordenada pelo módulo central main.py.

  A arquitetura do sistema é composta por quatro módulos principais, descritos a seguir com suas respectivas entradas, saídas e algoritmos de funcionamento:

  === Módulo de Ingestão

  ==== Entradas
  Repositório de código-fonte bruto.

  ==== Saídas
  Métodos estruturados e metadados.

  ==== Funcionamento: 
  Utiliza a biblioteca nativa ast (Abstract Syntax Tree) do Python para varrer os arquivos, extrair assinaturas de funções, docstrings e dependências mapeadas. Essa abordagem contorna as limitações da análise puramente textual, garantindo a extração precisa da topologia do código.

  === Módulo de Controle de Contexto

  ==== Entradas
  Método alvo a ser testado.

  ==== Saídas
  Trechos de código correlatos (nós de contexto).

  ==== Funcionamento
  Implementa o algoritmo de busca de similaridade vetorial (Cosine Similarity) no banco de dados Qdrant. Na fase de Linha de Base, este módulo é suprimido. Na fase Principal (RAG), ele é responsável por buscar as dependências externas e classes necessárias ao teste do método alvo.

  === Módulo de Geração e Reparo

  ==== Entradas
  Método alvo, contexto recuperado (se aplicável) e feedback de erro (em caso de falha iterativa).

  ==== Saídas
  Código do teste unitário.

  ==== Funcionamento
  Atua como um agente autônomo. O LLM propõe um teste inicial; caso a execução falhe, o agente ingere a tipologia do erro (ex: stack trace) e ajusta iterativamente o prompt em um ciclo de tuning, até que o código seja aprovado ou atinja o limite máximo de tentativas estabelecido.

  === Módulo de Medição e Execução

  ==== Entradas
  Código do teste candidato.

  ==== Saídas
  Status de execução (Pass/Fail) e métricas numéricas de cobertura.

  ==== Funcionamento
  Instancia um ambiente isolado (sandbox) para rodar o teste de forma segura, utilizando frameworks padrão da linguagem, como o pytest. Ao final da execução, o módulo registra o percentual de cobertura alcançado e cataloga eventuais exceções geradas pelo código.

  == Seleção da Amostra e Dados Usados
  Para garantir a validade externa do experimento, o sistema não é testado em fragmentos de código isolados, mas sim em repositórios open-source consolidados no ecossistema Python.

  Estes dados representam cenários do mundo real, contendo dependências inter-módulos, classes aninhadas e regras de negócio complexas, essenciais para testar o limite da janela de contexto do LLM. A amostra foi gerada através do módulo parser.py, que filtrou o repositório utilizando critérios baseados em AST. Foram excluídos métodos triviais (como `__init__` simples ou getters/setters) e selecionados métodos com complexidade ciclomática moderada a alta. O experimento utilizou um conjunto de 184 métodos alvo, extraídos de 2 repositórios distintos, gerando um volume de testes suficiente para análise estatística.

  == Métricas de Avaliação
  As métricas foram selecionadas para avaliar tanto a qualidade do produto gerado quanto o esforço computacional da ferramenta. Os resultados extraídos pelo main.py serão submetidos às seguintes equações:

  === Taxa de Sucesso (Pass Rate - PR)
  Mede a proporção de testes que compilam e passam com sucesso na primeira asserção válida, sem gerar erros de sintaxe ou importação. Observa-se a capacidade do modelo de gerar código pronto para uso.

  $ "PR" = ("T_pass" / "T_total") * 100 $ <eq:taxa-de-sucesso>

  Onde T_pass é o número de testes aprovados e T_total é o total de métodos avaliados na amostra.

  === Cobertura de Código (Code Coverage - CC)
  Indicador primário da qualidade funcional. Avalia o percentual de linhas do código original que foram efetivamente exercitadas pelo teste gerado.

  $ "CC" = ("L_exec" / "L_total") * 100 $ <eq:cobertura-de-codigo>

  Onde L_exec representa as linhas de código executadas durante o teste e L_total é o número total de linhas do método alvo.

  === Esforço de Reparo ou Autonomia (Repair Effort -RE)
  Mede o custo computacional do ciclo de tuning. Representa a média de iterações que o módulo repair.py precisou executar até aprovar o código. Uma métrica menor indica maior resiliência e precisão no prompt inicial.

  $ "RE" = 1 / N sum_(i=1)^N I_i $ <eq:esforco-de-reparo>

  Onde N é o total de métodos e I_i é o número de iterações gastas no método i.

  == Abordagem de Coleta de Dados
  A coleta de dados ocorrerá em um ambiente controlado, utilizando a própria arquitetura como instrumento de medição. O experimento será dividido em duas fases rigorosas sobre o mesmo conjunto de dados:

  1. Linha de Base (Baseline - Contexto Estático): O sistema processará a amostra com o módulo retriever.py desativado. O LLM receberá em seu prompt apenas a assinatura e o corpo isolado do método extraído via AST.

  2. Fase Principal (Abordagem RAG): O experimento é reiniciado, ativando a integração com o Qdrant. O LLM receberá o método alvo acrescido dos nós vetoriais recuperados (dependências externas, importações e declarações de classes).

  Ao final da execução de ambas as fases, o componente de orquestração compilará as métricas (PR, CC e RE) cruzando os dados de cada fase em um arquivo tabular (JSON/CSV), permitindo a análise quantitativa que responderá às questões de pesquisa propostas.
] 
