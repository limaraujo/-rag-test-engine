#let conclusion = [
  = Conclusão

  Este trabalho apresentou uma arquitetura Python para geração automática de
  testes unitários que integra três componentes: análise estática via AST,
  recuperação de contexto dinâmico por similaridade vetorial (RAG com Qdrant)
  e um ciclo de reparo autônomo guiado por feedback de execução do pytest.
  O sistema foi avaliado experimentalmente sobre dois repositórios open-source
  com perfis de complexidade distintos.

  Os resultados confirmam parcialmente as hipóteses iniciais. *No PyJWT*, repositório
  de alta complexidade com forte interdependência entre módulos criptográficos, o
  RAG proporcionou ganho expressivo: o perfil `rag-completo` elevou a taxa de
  símbolos válidos de 71,4% para 81,0% (+9,6 p.p.) e o `rag-limitado` reduziu
  a necessidade de iterações de reparo, com 60,3% de testes aprovados já na
  primeira geração frente a 52,4% na linha de base.

  *Nos Code Katas*, repositório de algoritmos autocontidos, o RAG gerou ganhos 
  apenas marginais na taxa de sucesso (elevando de 81,0% para 82,8%) e manteve a 
  cobertura estável, que já era elevada sem contexto adicional (~99%), mas o cache 
  de geração demonstrou eficácia de 16,9% na redução de chamadas ao LLM na segunda passagem.

  As principais conclusões são:

  - O impacto do RAG é *proporcional ao acoplamento* do repositório: quanto mais
    o código-alvo depende de módulos externos, maior o benefício da injeção de
    contexto vetorial.
  - Existe um *ponto de retorno decrescente* no volume de contexto RAG: o perfil
    `rag-limitado` superou o `rag-completo` na taxa de primeira geração, sugerindo
    que snippets em excesso introduzem ruído e diluem a atenção do modelo.
  - As falhas persistentes são sistematicamente ligadas a *dependências de I/O
    externo* (criptografia, HTTP, arquivos) e não à falta de contexto textual,
    um limite intrínseco que o RAG não consegue superar sozinho.
  - A cobertura de linhas é alta e *insensível ao nível de RAG*, indicando que
    o benefício da abordagem está na executabilidade dos testes, não na
    profundidade das asserções geradas.

  Em síntese, a arquitetura proposta transforma a geração de testes unitários
  em um processo confiável e autônomo para repositórios Python de complexidade
  moderada a alta, com custo computacional controlável via cache e orçamento
  de contexto configurável.
]
