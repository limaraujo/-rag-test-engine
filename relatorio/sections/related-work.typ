#let related-work = [
  = Trabalhos Relacionados

  A geração automática de testes unitários evoluiu de abordagens baseadas em busca para métodos que integram modelos de linguagem. Esta seção revisa os trabalhos mais representativos de cada área que fundamentam esta pesquisa.

  == Geração de Testes por Busca (Baseline Python)
  Pynguin @lukasczyk2022pynguin é a ferramenta canônica para geração automática de suítes de teste em Python, aplicando análise de tipos e busca exploratória. Embora alcance alta cobertura estrutural em código autocontido, a ferramenta enfrenta limitações severas de legibilidade e falha ao lidar com dependências externas que requerem mocks semanticamente corretos, estabelecendo o teto que abordagens com LLM buscam superar.

  == Geração de Testes com LLMs
  TestPilot @schafer2023testpilot conduziu uma avaliação empírica sistemática do uso de modelos de linguagem para testes unitários em Python, identificando como a qualidade do prompt afeta a taxa de compilação dos testes gerados. Contudo, o contexto fornecido ao modelo é essencialmente estático, sem a recuperação dinâmica de dependências e da arquitetura do projeto.

  == Recuperação Aumentada (RAG) para Código
  Nashid et al. @nashid2023retrieval investigam a seleção de exemplos via recuperação vetorial para _few-shot learning_ aplicado a código. O estudo comprova que snippets recuperados por similaridade semântica superam consistentemente exemplos fixos no prompt. Esse resultado fundamenta a hipótese central deste trabalho sobre o valor da injeção de contexto dinâmico estruturado para mitigar alucinações.

  == Reparo Autônomo de Código
  Xia e Zhang @xia2023conversational demonstraram que LLMs conseguem atuar como agentes autônomos, corrigindo bugs reais iterativamente ao serem alimentados com as saídas de erro do compilador. Esse achado valida teoricamente a abordagem do ciclo autônomo de _tuning_ implementado neste trabalho.

  == Posicionamento do Trabalho
  A @tab:related sintetiza as principais características dos trabalhos relacionados e como o presente trabalho se diferencia.

  #figure(
    table(
      columns: (1.2fr, 0.9fr, 0.8fr, 0.8fr, 0.8fr),
      align: (left, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header(
        [*Trabalho*], [*LLM*], [*RAG*], [*Reparo*], [*Python*]
      ),
      table.hline(y: 1, stroke: 0.5pt),
      [Pynguin @lukasczyk2022pynguin],         [Não], [Não], [Não], [Sim],
      [TestPilot @schafer2023testpilot],       [Sim], [Não], [Não], [Sim],
      [Nashid et al. @nashid2023retrieval],    [Sim], [Sim], [Não], [Sim],
      [Xia & Zhang @xia2023conversational],    [Sim], [Não], [Sim], [Não],
      [*Este trabalho*],                       [*Sim*],[*Sim*],[*Sim*],[*Sim*],
      table.hline(y: 6, stroke: 0.5pt),
    ),
    caption: [Comparação com trabalhos relacionados.],
  ) <tab:related>

  A principal contribuição diferenciadora deste trabalho é a combinação de três elementos em um único pipeline: RAG com banco vetorial, análise estática via AST e ciclo de reparo autônomo baseado no feedback do Pytest.
]
