#let introduction = [
  = Introdução
  Testes unitários são fundamentais para a qualidade de software, mas sua criação consome esforço considerable dos desenvolvedores. Esse tempo dedicado à escrita de testes poderia ser alocado no desenvolvimento de novas funcionalidades.
  
  LLMs abrem oportunidades para automatizar a escrita de testes. Contudo, enfrentam limitações críticas: desconhecimento do domínio global do projeto e alucinação de código. Essas limitações resultam em testes que referenciam métodos ou variáveis inexistentes, gerando falhas em execução.

  A investigação deste problema é de grande interesse acadêmico e industrial, pois a criação de um mecanismo que automatize a geração de testes de forma confiável e semanticamente correta tem o potencial de reduzir drasticamente os custos de manutenção de software e elevar a cobertura de código, especialmente em bases de código complexas e colaborativas, como projetos open-source.

  Atualmente, as soluções existentes para automação de testes dividem-se em duas abordagens com limitações claras. As ferramentas tradicionais baseadas em busca (como fuzzers e geradores estáticos) conseguem alta cobertura, mas frequentemente produzem testes difíceis de ler e manter por humanos, carecendo de compreensão semântica. Por outro lado, o uso de LLMs de forma isolada (vanilla prompts) gera testes legíveis, mas o modelo fica restrito à janela de contexto imediata fornecida pelo usuário, ignorando as dependências e a arquitetura do ecossistema do software. É necessário, portanto, uma solução que una a precisão estrutural do código com o poder de generalização e contextualização dos modelos de linguagem.

  Para resolver esse problema, este trabalho propõe uma arquitetura que integra Análise Estática e Retrieval-Augmented Generation (RAG). A abordagem realiza a extração estruturada de métodos através de Abstract Syntax Tree (AST) e utiliza o banco de dados vetorial Qdrant para buscar dinamicamente o contexto exato necessário para o modelo. Além disso, a arquitetura incorpora um ciclo de agentes autônomos de reparo, que refinam iterativamente o código gerado com base no feedback de execução (erros e cobertura).

  As principais contribuições deste trabalho são:

  - Desenvolvimento de uma arquitetura híbrida: Integração de Análise Estática (AST) e memória vetorial (RAG) para fornecer contexto estruturado e preciso aos LLMs na geração de código em Python;

  - Implementação de um ciclo de reparo autônomo (tuning): Criação de agentes capazes de executar o código gerado, catalogar erros e refazer os testes de forma iterativa sem intervenção humana;

  - Avaliação empírica do impacto do contexto vetorial: Um experimento comparativo em projetos open-source que isola e mensura como a ativação do RAG afeta o esforço computacional (número de iterações de correção) e a qualidade funcional (taxa de sucesso e cobertura de código).
]