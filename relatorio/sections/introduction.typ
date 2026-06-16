#let introduction = [
  = Introdução
  
  Testes unitários são fundamentais para a qualidade e confiabilidade do software, mas sua criação consome esforço e tempo considerável dos desenvolvedores. A automação dessa tarefa representa uma oportunidade significativa para ampliar a cobertura de código e reduzir custos de manutenção, especialmente em bases de código extensas e complexas.
  
  Modelos de Linguagem de Grande Escala (LLMs) abriram novas possibilidades para automatizar a geração de testes através de prompting. Contudo, essas soluções enfrentam limitações críticas quando aplicadas a sistemas reais: (1) desconhecimento do contexto global do projeto, levando a referências de métodos ou variáveis inexistentes; (2) alucinação de comportamentos que não refletem a lógica real do código; (3) perda de qualidade semântica dos testes, resultando em métricas de cobertura enganosas que não garantem resiliência em produção.
  
  As abordagens existentes dividem-se em dois extremos com limitações claras. Ferramentas tradicionais baseadas em busca (_fuzzers_, geradores estáticos) conseguem cobertura alta, mas produzem testes difíceis de ler e manter, carecendo de compreensão semântica. Por outro lado, LLMs isolados (_vanilla prompts_) geram testes legíveis e conceitualmente corretos, mas são restritos à janela de contexto imediata, ignorando as dependências inter-módulos e a arquitetura real do sistema. É necessária, portanto, uma solução que combine a precisão estrutural da análise estática com o poder de generalização dos modelos de linguagem.
  
  Este trabalho propõe uma arquitetura integrada que combina Análise Estática e _Retrieval-Augmented Generation_ (RAG) em um motor automatizado de geração de testes pytest. O sistema implementa oito fases orquestradas: ingestão estruturada de símbolos, indexação vetorial, enriquecimento RAG com busca híbrida, geração de testes com LLM, execução com pytest, reparo autônomo baseado em feedback de erro, otimização de cobertura e validação de suíte completa. Integra adicionalmente cache persistente de gerações aprovadas e rastreamento detalhado de custos computacionais (tokens, iterações).
  
  As principais contribuições deste trabalho são:
  
  - Arquitetura híbrida funcional: Integração de Análise Estática (AST) e memória vetorial (RAG) com busca híbrida que combina similaridade vetorial, call graph e dependency graph, fornecendo contexto estruturado e dinâmico aos LLMs na geração de código Python.
  
  - Pipeline de automação completo em produção: Sistema com ingestão robusta, indexação incremental, geração parametrizável (perfis sem-rag, rag-limitado, rag-completo, com-cache), cache de gerações aprovadas, reparação iterativa sem intervenção humana, análise automática de cobertura, e rastreamento detalhado de custos, permitindo operação eficiente em repositórios reais.
  
  - Avaliação empírica comparativa: Experimento que mensura isoladamente o impacto do RAG versus baseline (sem RAG), medindo Taxa de Sucesso, Cobertura de Código e Esforço de Reparo, e analisando trade-offs entre os quatro perfis implementados.
]