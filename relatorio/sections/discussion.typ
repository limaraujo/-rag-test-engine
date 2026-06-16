#let discussion = [
  = Discussão

  Esta seção interpreta os resultados à luz das questões de pesquisa definidas
  na metodologia, discute os padrões observados, as limitações dos experimentos
  e as implicações práticas da abordagem proposta.

  == QP1: Impacto do RAG na Taxa de Sucesso

  Os resultados confirmam que o RAG melhora a taxa de sucesso de forma
  dependente do contexto do repositório. No PyJWT, o `rag-completo` superou o
  `sem-rag` em 9,6 pontos percentuais (81,0% vs. 71,4%), respondendo
  afirmativamente à QP1 nesse cenário.

  No entanto, o impacto foi quase nulo nos Code Katas, onde a linha de base obteve 
  81,0% e a variante `rag-completo` alcançou apenas 82,8%. Esse contraste revela um 
  princípio de necessidade de contexto: o RAG só agrega valor quando o LLM genuinamente 
  carece de informações externas ao corpo do método para construir um teste válido.

  No PyJWT, os algoritmos criptográficos referenciam chaves, formatos de serialização 
  JWK e classes auxiliares distribuídas em múltiplos módulos, precisamente o tipo de
  dependência que o retriever vetorial consegue fornecer. Nos Code Katas, as
  funções são autocontidas; o acréscimo de snippets RAG não elimina as falhas
  estruturais (dependências de arquivos externos e I/O de rede) que nenhum
  nível de contexto textual poderia resolver.

  Um dado revelador é que nenhum símbolo foi exclusivamente salvo pelo perfil
  `sem-rag` em nenhum dos dois repositórios. Isso indica que o RAG, mesmo
  quando não melhora a taxa agregada, não prejudica a geração de testes para
  funções que o LLM já consegue testar sem auxílio.

  == QP2: RAG e Redução do Esforço de Reparo

  A métrica de *1ª Geração* operacionaliza indiretamente o esforço de reparo:
  quanto maior a fração de testes aprovados sem iterações de correção, menor o
  custo computacional autônomo. No PyJWT, o `rag-limitado` obteve o melhor
  resultado nessa dimensão (60,3%), contra 52,4% do `sem-rag`, representando
  15% mais testes gerados corretamente de imediato.

  Interessantemente, o `rag-completo` ficou abaixo do `rag-limitado` na taxa
  de primeira geração (54,0% vs. 60,3%), sugerindo que um volume excessivo de
  contexto RAG pode comprometer a precisão do prompt inicial. Esse fenômeno é
  conhecido na literatura como context dilution: quando o prompt contém
  muito conteúdo irrelevante, o modelo desloca atenção dos elementos centrais
  da tarefa @nashid2023retrieval. O perfil `rag-limitado`, com orçamento de
  contexto reduzido, forçou uma seleção mais rigorosa dos snippets mais
  relevantes, resultando em um prompt mais focado e maior taxa de sucesso na
  primeira tentativa.

  Nos Code Katas, as taxas de primeira geração foram estáveis entre os perfis
  (74,1%–77,6%), reforçando a hipótese de que, nesse repositório, o fator
  limitante não é o contexto mas sim a natureza das dependências externas
  irresolvíveis.

  == QP3: Impacto na Cobertura de Código

  A cobertura de linhas foi alta e homogênea em ambos os repositórios,
  variando entre 84,4% e 86,5% no PyJWT e entre 96,9% e 99,8% nos Code Katas.
  A diferença entre perfis é marginal (máximo de 2,1 p.p. no PyJWT) e não
  segue uma tendência monotônica com o nível de RAG.

  Isso leva à conclusão de que a cobertura é determinada principalmente pela
  qualidade das asserções geradas pelo LLM, algo que não muda substancialmente
  com o nível de contexto vetorial. O RAG melhora a executabilidade do teste
  (o teste compila e roda), mas não necessariamente a profundidade com que
  ele explora o código. Elevar a cobertura exigiria técnicas complementares,
  como detecção explícita de branches não cobertos e regeneração dirigida,
  funcionalidade parcialmente implementada no módulo `coverage_cycle.py` mas
  que não foi ativada no experimento principal.

  == Análise das Falhas Persistentes

  As falhas que resistiram a todos os perfis e iterações de reparo podem ser
  agrupadas em três categorias:

  1. Dependências criptográficas brutas: Métodos como `RSAAlgorithm.from_jwk`
  e `ECAlgorithm.to_jwk` exigem chaves criptográficas em formato específico
  (PEM, DER) que o LLM não consegue instanciar corretamente. O RAG fornece
  o contexto estrutural, mas não substitui a necessidade de _fixtures_ concretas
  com material criptográfico válido.

  2. Dependências de I/O externo: Funções que fazem requisições HTTP
  (`PyJWKClient.fetch_data`) ou leem arquivos CSV (`calculate_distance`,
  `create_graph`) falham porque o LLM não consegue inferir o formato exato dos
  dados externos. Esses casos demandariam mocks de infraestrutura que o agente
  autônomo atual não é capaz de construir.

  3. Erros de sintaxe persistentes: Alguns símbolos apresentaram erros de
  parsing na saída do LLM (`closing parenthesis '}' does not match '['`)
  mesmo após o ciclo de reparo, indicando que certos padrões de código
  (dicionários aninhados complexos) induzem erros sistemáticos no modelo que
  não são corrigíveis com apenas 2 iterações.

  == Efetividade do Cache

  O contraste na eficácia do cache entre os repositórios é notável: 16,9% de
  redução nos Code Katas versus 1,1% no PyJWT. A chave é a homogeneidade dos
  símbolos: em repositórios algorítmicos com padrões repetitivos (ex.: múltiplos
  métodos de travessia em estruturas de dados), o cache de geração evita chamadas
  ao LLM com expressivo impacto econômico. Em bibliotecas com alta especificidade
  por símbolo, como o PyJWT, o benefício é marginal. Isso implica que o retorno do investimento em cache é proporcional à redundância
  semântica do repositório. Para equipes com grandes bases de código, o cache
  pode representar economia significativa nas iterações contínuas do pipeline.

  == Limitações do Experimento

  Algumas limitações devem ser consideradas na interpretação dos resultados:

  - Amostra restrita: Dois repositórios cobrem apenas uma fração do espectro de
    estilos e domínios de código Python. Resultados podem variar em domínios como
    ciência de dados, frameworks web ou sistemas embarcados.
  - Modelo único: Todos os experimentos utilizaram `gpt-5-nano`. Modelos com
    janela de contexto maior ou treinamento específico para código podem apresentar
    comportamento distinto em relação ao RAG.
  - Limite de reparo fixo: O ciclo de reparo autônomo foi limitado a 2 iterações.
    Aumentar esse limite poderia recuperar parte dos símbolos que
    falharam com erros de sintaxe persistentes.
  - Ausência de avaliação semântica: As métricas utilizadas (taxa de sucesso
    e cobertura) mensuram executabilidade e alcance estrutural, mas não garantem
    que os testes verificam comportamentos corretos. Uma análise de mutation testing
    forneceria evidências mais robustas da qualidade das asserções.
]
