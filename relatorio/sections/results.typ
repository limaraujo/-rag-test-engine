#let results = [
  = Resultados

  Esta seção apresenta os resultados quantitativos obtidos ao executar o
  pipeline nos dois repositórios selecionados. As métricas foram coletadas
  automaticamente pelo módulo de orquestração e consolidadas nos artefatos
  `run_summary.json` de cada execução.

  == Repositório 1: PyJWT

  A biblioteca PyJWT é uma implementação Python amplamente utilizada do padrão
  JSON Web Tokens (RFC 7519), caracterizada por forte interdependência entre
  módulos, uso intenso de criptografia (RSA, EC, OKP, HMAC) e abstrações
  polimórficas. Foram extraídos *126 símbolos* elegíveis para geração (funções
  e métodos), após filtragem das 39 classes presentes nos 12 arquivos analisados.

  Os resultados por perfil de execução são apresentados na @tab:jwt-resumo.

  #figure(
    table(
      columns: (1.4fr, 0.7fr, 0.7fr, 0.8fr, 0.8fr, 0.9fr, 1fr),
      align: (left, center, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header(
        [*Perfil*], [*Salvos*], [*Falharam*], [*Válidos %*],
        [*1ª Gen %*], [*Aprovação %*], [*Cob. Linhas*]
      ),
      table.hline(y: 1, stroke: 0.5pt),
      [`sem-rag`],      [82], [44], [71,4%], [52,4%], [100%], [86,5%],
      [`rag-limitado`], [95], [31], [80,2%], [60,3%], [100%], [85,6%],
      [`rag-completo`], [96], [29], [81,0%], [54,0%], [100%], [84,4%],
      [`com-cache`],    [92], [34], [77,8%], [56,3%], [100%], [84,5%],
      table.hline(y: 5, stroke: 0.5pt),
    ),
    caption: [Resultados por perfil, PyJWT (126 símbolos).],
  ) <tab:jwt-resumo>

  O perfil `rag-completo` obteve o maior número de testes salvos (96) e a
  maior taxa de símbolos válidos (81,0%), representando uma melhoria de *9,6
  pontos percentuais* em relação à linha de base `sem-rag` (71,4%). O perfil
  `rag-limitado`, com orçamento de contexto reduzido, já entregou ganho
  expressivo (80,2%), indicando que mesmo uma quantidade moderada de contexto
  vetorial é suficiente para impactar a geração.

  O indicador *1ª Geração* aponta a fração de símbolos cujo teste foi aprovado
  diretamente pelo LLM, sem iterações de reparo. O `rag-limitado` obteve o
  melhor desempenho nessa métrica (60,3%), superando o `sem-rag` em 7,9 p.p.
  Isso evidencia que o contexto RAG reduz a necessidade de ciclos de correção
  autônoma. Curiosamente, o `rag-completo` ficou abaixo do `rag-limitado`
  nessa métrica (54,0%), possivelmente pelo excesso de contexto interferindo na
  objetividade do prompt.

  A cobertura de linhas manteve-se elevada e relativamente estável entre 84,4%
  e 86,5%, sem diferença estatisticamente expressiva entre os perfis. Isso
  sugere que o RAG melhora a taxa de compilação e execução dos testes, mas não
  impacta diretamente a densidade de cobertura após o teste ser gerado.

  *Falhas persistentes.* Treze símbolos falharam em todos os quatro perfis,
  predominantemente métodos criptográficos que exigem chaves RSA/EC reais ou
  acesso a endpoints HTTP: `RSAAlgorithm.from_jwk`, `RSAAlgorithm.to_jwk`,
  `ECAlgorithm.to_jwk`, `HMACAlgorithm.prepare_key`,
  `PyJWKClient.get_jwk_set`, entre outros. Esses símbolos demandam mocks
  complexos de infraestrutura que o LLM não consegue instanciar corretamente
  sem exemplos concretos.

  === Eficiência de Cache, PyJWT

  O perfil `com-cache` executou duas passagens sobre o mesmo conjunto para
  avaliar o aproveitamento do cache de geração, conforme @tab:jwt-cache.

  #figure(
    table(
      columns: (1.6fr, 1fr, 1fr),
      align: (left, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Métrica*], [*1ª Passagem (fria)*], [*2ª Passagem (quente)*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Tokens consumidos], [868.566], [859.228],
      [Chamadas LLM],      [157],     [154],
      [Cache hits],        [0],       [0],
      [LLM evitadas],      [-],       [0],
      [Redução de tokens], [-],       [*1,1%*],
      table.hline(y: 6, stroke: 0.5pt),
    ),
    caption: [Benchmark de cache, PyJWT.],
  ) <tab:jwt-cache>

  O cache teve eficácia mínima no PyJWT (1,1% de redução, zero hits). Isso se
  deve à natureza do repositório: cada símbolo criptográfico possui assinatura
  e corpo muito distintos, gerando hashes de cache únicos que não se repetem
  entre execuções.

  == Repositório 2: Code Katas

  O repositório Code Katas reúne implementações algorítmicas independentes
  (grafos, estruturas de dados, algoritmos de busca), caracterizadas por baixo
  acoplamento inter-módulo e lógica autocontida. Foram extraídos *58 símbolos*
  elegíveis.

  Os resultados estão consolidados na @tab:katas-resumo.

  #figure(
    table(
      columns: (1.4fr, 0.7fr, 0.7fr, 0.8fr, 0.8fr, 0.9fr, 1fr),
      align: (left, center, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header(
        [*Perfil*], [*Salvos*], [*Falharam*], [*Válidos %*],
        [*1ª Gen %*], [*Aprovação %*], [*Cob. Linhas*]
      ),
      table.hline(y: 1, stroke: 0.5pt),
      [`sem-rag`],      [47], [11], [81,0%], [75,9%], [100%], [99,2%],
      [`rag-limitado`], [47], [11], [81,0%], [77,6%], [100%], [98,8%],
      [`rag-completo`], [48], [10], [82,8%], [74,1%], [100%], [99,8%],
      [`com-cache`],    [47], [11], [81,0%], [75,9%], [100%], [96,9%],
      table.hline(y: 5, stroke: 0.5pt),
    ),
    caption: [Resultados por perfil, Code Katas (58 símbolos).],
  ) <tab:katas-resumo>

  Diferentemente do PyJWT, as métricas de validade e primeira geração
  permaneceram estáveis entre os perfis, com a taxa de símbolos válidos
  idêntica (81,0%) para `sem-rag`, `rag-limitado` e `com-cache`.
  O `rag-completo` apresentou leve vantagem: 48 símbolos salvos contra 47
  nos demais, o que equivale a recuperar um símbolo que falhou em todos os outros perfis.

  A cobertura de linhas foi consistentemente alta, próxima de 99%, com o pico
  de 99,8% no `rag-completo`. Esses resultados indicam que, para código
  algorítmico autocontido, o LLM já dispõe de contexto suficiente na própria
  assinatura e corpo do método, e o RAG não acrescenta ganho significativo.

  *Falhas persistentes.* Nove símbolos falharam em todos os perfis: os
  relacionados à classe `Autocomplete` (que depende de um arquivo de dados
  externos não incluído no repositório), funções de acesso à rede (`get_json`,
  `lat_long_dict`, `flight_path`) e funções que requerem arquivos CSV
  externos (`calculate_distance`, `create_graph`). Todas as falhas são
  atribuíveis a dependências de I/O externas, não cobertas pelo contexto RAG.

  === Eficiência de Cache, Code Katas

  #figure(
    table(
      columns: (1.6fr, 1fr, 1fr),
      align: (left, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Métrica*], [*1ª Passagem (fria)*], [*2ª Passagem (quente)*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Tokens consumidos], [237.656], [197.487],
      [Chamadas LLM],      [64],      [52],
      [Cache hits],        [0],       [12],
      [LLM evitadas],      [-],       [12],
      [Redução de tokens], [-],       [*16,9%*],
      table.hline(y: 6, stroke: 0.5pt),
    ),
    caption: [Benchmark de cache, Code Katas.],
  ) <tab:katas-cache>

  O cache foi expressivamente eficaz nos Code Katas: na segunda passagem, 12
  chamadas LLM foram evitadas (18,75% do total), com redução de 16,9% nos
  tokens consumidos. A maior eficácia em relação ao PyJWT explica-se pela
  menor variabilidade dos símbolos: métodos algorítmicos similares geram hashes
  de cache idênticos ou próximos, aumentando as colisões benéficas.

  == Comparação entre Repositórios

  A @tab:comparacao sintetiza o impacto do RAG nos dois contextos experimentais.

  #figure(
    table(
      columns: (1.8fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header(
        [*Repositório*], [*Baseline válidos*], [*RAG-completo válidos*],
        [*Ganho*], [*Cob. (RAG)*]
      ),
      table.hline(y: 1, stroke: 0.5pt),
      [PyJWT (alta complexidade)],       [71,4%], [81,0%], [*+9,6 p.p.*], [84,4%],
      [Code Katas (baixa complexidade)], [81,0%], [82,8%], [*+1,8 p.p.*], [99,8%],
      table.hline(y: 3, stroke: 0.5pt),
    ),
    caption: [Impacto do RAG por perfil de complexidade do repositório.],
  ) <tab:comparacao>

  O padrão é claro: o RAG agrega valor proporcional à complexidade de dependências
  do código-alvo. Em repositórios com forte acoplamento inter-módulo, a injeção
  de contexto vetorial é determinante para a correta geração de mocks e imports.
  Em código algorítmico autocontido, o LLM já dispõe das informações necessárias
  e o RAG tem impacto neutro.
]
