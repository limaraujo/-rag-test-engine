#let motivation = [
  = Motivação
  A adoção de Modelos de Linguagem de Grande Escala (LLMs) tem demonstrado um grande potencial na automação de tarefas de Engenharia de Software, especialmente na geração de código. Contudo, sua aplicação direta na criação de testes unitários para sistemas reais enfrenta obstáculos arquiteturais e conceituais.

  Para ilustrar o problema, considere este cenário: Um desenvolvedor pede a um LLM que crie um teste para o método processar_pagamento() da classe CarrinhoDeCompras. O modelo gera um teste sintaticamente correto analisando apenas a classe isolada. Porém, a classe importa um utilitário externo (ex: from utils.taxas import calcular_imposto_regional) não incluído no prompt. Sem acesso a esse contexto global, o LLM alucina um comportamento ou omite o mock necessário para a dependência externa.

  Esse cenário evidencia três limitações críticas:
  - Projetos reais formam ecossistemas profundamente interconectados. Inserir todos os arquivos no prompt é tecnicamente inviável (limite de tokens) e financeiramente custoso.
  - Abordagens tradicionais (vanilla prompts) tratam o código como texto plano, sem compreender formalmente a árvore de dependências, heranças e assinaturas de métodos.
  - Excesso de contexto irrelevante diminui a precisão do modelo ao recuperar a informação necessária para o teste específico.

  A dependência exclusiva do LLM sem contexto gera consequências prejudiciais:
  - O código gerado frequentemente falha na primeira execução (NameError, ImportError). O desenvolvedor gasta mais tempo depurando o código sugerido do que teria gastado escrevendo-o do zero.
  - LLMs podem alucinar mocks que fazem testes passar, ignorando as regras de negócio reais. Isso gera métricas de cobertura "vazias" que não garantem qualidade ou resiliência em produção.

  Assim, a motivação deste trabalho reside na necessidade de construir uma ponte entre a capacidade generativa dos LLMs e o rigor estrutural dos repositórios de código. O uso combinado de Análise Estática e Retrieval-Augmented Generation permitem compreender as dependências reais e injetar apenas contexto útil no prompt, transformando a geração automatizada de testes em uma ferramenta autônoma e confiável.
]