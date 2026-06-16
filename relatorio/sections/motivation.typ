#let motivation = [
  = Motivação
  
  A adoção de Modelos de Linguagem de Grande Escala (LLMs) tem demonstrado grande potencial na automação de tarefas de Engenharia de Software, especialmente na geração de código. Contudo, sua aplicação direta na criação de testes unitários para sistemas reais enfrenta obstáculos arquiteturais e conceituais que persistem mesmo em abordagens iniciais com RAG.
  
  Esse cenário evidencia três limitações críticas que motivam o trabalho:
  
  - Projetos reais formam ecossistemas profundamente interconectados, mas inserir todos os arquivos no prompt é tecnicamente inviável (limite de tokens) e financeiramente custoso. Abordagens vanilla (contexto estático isolado) carecem de compreensão da topologia real, dependências entre módulos, heranças, assinaturas de métodos são vistas apenas como texto plano.
  
  - Recuperar muitos trechos de código (RAG ingênuo) para enriquecer o prompt frequentemente piora a precisão do modelo, pois o LLM gasta capacidade processando informação periférica. Além disso, trechos duplicados ou desnecessários inflam o custo computacional.
  
  - Mesmo quando um teste passa (sem erros de sintaxe ou importação), ele pode não exercitar adequadamente o código. O LLM alucina mocks superficiais que fazem assertions triviais passar, gerando métricas de cobertura "vazias" que não garantem qualidade ou resiliência em produção.
  
  Além dessas limitações arquiteturais, o ciclo de integração entre LLM e repositório real revela problemas operacionais ignorados por abordagens iniciais:
  
  - O modelo frequentemente produz imports com caminhos absolutos ou módulos inexistentes, causando ModuleNotFoundError na primeira execução. Esses erros exigem correção manual, anulando a automação.
  
  - Quando um teste falha por NameError ou ImportError, abordagens simples regeneram desde o início. Contudo, um agente especializado em reparo que injeta o stack trace do pytest no prompt consegue resolver a maioria das falhas iterativamente e com precisão, sem overhead de re-geração.
  
  - Sem mecanismo de parametrização, cada repositório gera um custo único e não otimizável. Soluções reais precisam balancear qualidade (cobertura, taxa de sucesso) contra custo (tokens LLM, iterações), oferecendo múltiplos perfis de trade-off.
  
  - Em repositórios com dezenas ou centenas de funções, testes gerados para símbolos similares são frequentemente regenerados do zero, multiplicando custos sem ganho de qualidade. Um mecanismo de cache inteligente que reutiliza testes já aprovados economiza 3-5x de custos LLM sem degradar resultados.
  
  Assim, a motivação deste trabalho reside em construir uma solução operacional e parametrizável que integre Análise Estática, RAG com busca híbrida (combinando similaridade vetorial com grafos de dependências e chamadas), e um pipeline iterativo com múltiplos agentes especializados: (1) um gerador que enriquece prompts com contexto dinâmico e preciso; (2) um reparador autônomo que corrige falhas específicas injetando feedback de erro; (3) um analisador de cobertura que identifica testes vazios e regenera iterativamente. A solução proposta endereça não apenas o desafio teórico de enriquecer contexto, mas também os desafios práticos de operacionalizar a geração automática de testes em repositórios reais, heterogêneos e de larga escala.
]