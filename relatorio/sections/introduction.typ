#let introduction = [
  = Introdução
  
  Testes unitários são fundamentais para a qualidade e confiabilidade do software, mas sua criação consome esforço e tempo considerável dos desenvolvedores. A automação dessa tarefa representa uma oportunidade significativa para ampliar a cobertura de código e reduzir custos de manutenção, especialmente em bases de código extensas e complexas.
  
  Modelos de Linguagem de Grande Escala (LLMs) abriram novas possibilidades para automatizar a geração de testes através de prompting. Contudo, essas soluções enfrentam limitações críticas quando aplicadas a sistemas reais: (1) desconhecimento do contexto global do projeto, levando a referências de métodos ou variáveis inexistentes; (2) alucinação de comportamentos que não refletem a lógica real do código; (3) perda de qualidade semântica dos testes, resultando em métricas de cobertura enganosas que não garantem resiliência em produção.
  
  As abordagens existentes dividem-se em dois extremos com limitações claras. Ferramentas tradicionais baseadas em busca (_fuzzers_, geradores estáticos) conseguem cobertura alta, mas produzem testes difíceis de ler e manter, carecendo de compreensão semântica. Por outro lado, LLMs isolados (_vanilla prompts_) geram testes legíveis e conceitualmente corretos, mas são restritos à janela de contexto imediata, ignorando as dependências inter-módulos e a arquitetura real do sistema. É necessária, portanto, uma solução que combine a precisão estrutural da análise estática com o poder de generalização dos modelos de linguagem.
  
  Este trabalho propõe uma arquitetura integrada que combina Análise Estática e _Retrieval-Augmented Generation_ (RAG) em um motor automatizado de geração de testes pytest em Python. O sistema realiza a extração estruturada de métodos via _Abstract Syntax Tree_ (AST), indexa símbolos no banco de dados vetorial Qdrant, enriquece o contexto através de busca híbrida (vetorial + grafos) em tempo real, e implementa um pipeline de automação completo com múltiplos agentes especializados: um gerador de testes, um reparador autônomo que corrige falhas iterativamente baseado em feedback de execução, um analisador de cobertura que regenera testes conforme necessário, além de mecanismos de cache inteligente e rastreamento detalhado de custos computacionais.
  
  As principais contribuições deste trabalho são:
  
  - Desenvolvimento de uma arquitetura híbrida funcional: Integração de Análise Estática (AST) e memória vetorial (RAG) com busca híbrida para fornecer contexto estruturado e dinâmico aos LLMs na geração de código Python, com suporte a múltiplos modelos e configurações de orçamento (sem-rag, rag-limitado, rag-completo);
  
  - Implementação de um pipeline de automação completo em produção: Sistema de geração com cache persistente, reparação iterativa sem intervenção humana, análise automática de cobertura de código, rastreamento detalhado de custo computacional (tokens LLM, iterações de reparo), e execução segura em ambientes isolados, permitindo operação eficiente em repositórios reais de qualquer escala;
  
  - Avaliação empírica comparativa: Experimento em dois repositórios open-source consolidados (PyJWT, code-katas) que isola e mensura o impacto do RAG versus linha de base (sem RAG), analisando Taxa de Sucesso (_pass rate_), Cobertura de Código, Esforço de Reparo (iterações), e custo computacional (tokens), com análise de trade-offs entre os quatro perfis de teste implementados.
]