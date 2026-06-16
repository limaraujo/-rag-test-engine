#let future-work = [
  = Trabalhos Futuros

  Os experimentos realizados apontam direções concretas de evolução para o
  sistema proposto:

  *Recuperação baseada em grafos.* O retriever atual utiliza exclusivamente
  similaridade vetorial para selecionar snippets de contexto. Integrar o grafo
  de chamadas (`call_graph.json`) como sinal primário de recuperação, priorizando
  callers e callees diretos do método alvo, permitiria fornecer ao LLM
  exatamente as dependências estruturais necessárias, em detrimento de funções
  apenas semanticamente similares. O módulo `hybrid.py` já computa um score
  híbrido, mas os pesos poderiam ser calibrados por aprendizado supervisionado
  sobre os resultados de execução.

  *Geração dirigida por cobertura.* O ciclo de cobertura (`coverage_cycle.py`)
  está implementado mas não foi ativado nos experimentos. Ativar a regeneração
  automática de testes quando a cobertura está abaixo de um limiar, injetando
  as linhas não cobertas como hint no prompt, é uma extensão direta que poderia
  elevar a cobertura de 84% para próximo de 95% no PyJWT.

  *Suporte a fixtures automáticas.* A categoria mais frequente de falhas
  persistentes são métodos que exigem material criptográfico (chaves RSA, EC)
  ou mocks de serviços HTTP. Desenvolver um módulo que detecte automaticamente
  essas dependências via análise de tipos e gere fixtures reutilizáveis permitiria
  atacar diretamente os 13 símbolos irresolvíveis do PyJWT.

  *Expansão para múltiplas linguagens.* A arquitetura modulariza o parser AST
  em `parsers/source/`, mas a implementação atual é exclusiva para Python.
  Substituir o parser por um baseado em Tree-sitter permitiria suporte a
  TypeScript, Java e Rust com o mesmo pipeline de geração e reparo.

  *Avaliação por mutation testing.* As métricas utilizadas (taxa de sucesso e
  cobertura de linhas) mensuram executabilidade mas não a qualidade semântica
  das asserções. Aplicar mutation testing (ex.: com MutPy ou Mutmut) sobre os
  testes gerados forneceria uma métrica de _mutation score_ que captura com
  maior precisão se o teste detecta regressões reais no código.

  *Cache semântico com embeddings.* O cache atual é baseado em hash exato do
  código-fonte. Um cache semântico que use a proximidade vetorial para recuperar
  testes gerados anteriormente para símbolos similares poderia ampliar
  significativamente a taxa de cache hits em repositórios com padrões repetitivos,
  reduzindo o custo em cenários de integração contínua com múltiplas execuções
  diárias.
]
