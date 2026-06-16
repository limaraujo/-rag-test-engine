#import "@preview/charged-ieee:0.1.4": ieee
#import "@preview/lovelace:0.3.0": *
#import "sections/abstract.typ": abstract
#import "sections/introduction.typ": introduction
#import "sections/motivation.typ": motivation
#import "sections/methodology.typ": methodology
#import "sections/results.typ": results
#import "sections/discussion.typ": discussion
#import "sections/related-work.typ": related-work
#import "sections/conclusion.typ": conclusion
#import "sections/future-work.typ": future-work

#show: ieee.with(
  title: [Integração de Análise Estática e Retrieval-Augmented Generation para geração de Testes Unitários com LLMs],
  abstract: abstract,
  authors: yaml("authors.yml"),
  bibliography: bibliography("refs.bib"),
)

#introduction

#motivation

#methodology

#results

#discussion

#related-work

#conclusion

#future-work

#show bibliography: set std.bibliography(title: text(10pt)[Referências])

= Modelo Typst
Apresentar alguns dos artigos existentes na literatura sobre o tema que está sendo trabalhado, suas *principais contribuições e limitações*.

Este é um exemplo de citação @IEEEhowto:kopka.

É interessante apresentar uma tabela no final desta seção sumarizando os artigos citados anteriormente, suas vantagens, contribuições e desvantagens. Na @tab:tabela-exemplo é apresentado um exemplo de tabela.

#figure(
  table(
    columns: (1.2fr, 1fr, 1fr, 1fr),
    align: (left, left, center, center),
    stroke: none,
    table.hline(y: 0, stroke: 0.5pt),
    table.header([*Módulos*], [*Entradas*], [*Saídas*], [*Algoritmo*]),
    table.hline(y: 1, stroke: 0.5pt),
    [Trabalho A], [Método X], [A], [D],
    [Trabalho B], [Método Y], [G], [J],
    table.hline(y: 3, stroke: 0.5pt),
  ),
  caption: [Exemplo de tabela],
) <tab:tabela-exemplo>

Na @fig:logo-cin é apresentado um exemplo de figura com a logo do centro de informática.

#figure(
  image("imagens/logo_cin_ufpe.png", width: 80%),
  caption: [Logo do centro.],
) <fig:logo-cin>

No @alg:cap é apresentado um exemplo de algoritmo.

#figure(
  kind: "algorithm",
  supplement: [Alg.],
  pseudocode-list[
    - *Require* $n >= 0$
    - *Ensure* $y = x^n$
    - $y <- 1$
    - $X <- x$
    - $N <- n$
    - *while* $N != 0$ *do*
      - *if* $N$ is even *then*
        - $X <- X times X$
        - $N <- N / 2$ #h(1em) // Exemplo de comentário
      - *else*
        - $y <- y times X$
        - $N <- N - 1$
  ],
  caption: [Algoritmo com legenda],
) <alg:cap>

== Resultados reprodução do artigo de referência

- Nos dados usados pelo artigo de referência
- No novo conjunto de dados escolhido

Utilizar gráficos e tabelas. Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

== Resultados proposta de melhoria do artigo de referência (CASO FEITA)

- Nos dados usados pelo artigo de referência
- No novo conjunto de dados escolhido

Utilizar gráficos e tabelas. Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

Comparar e discutir os resultados da proposta de melhoria com os resultados obtidos com a reprodução do artigo de referência.

= Conclusões e trabalhos futuros

Conclusão, principais limitações e problemas do sistema proposto pelo artigo de referência e pela proposta de melhoria (CASO FEITA), e trabalhos futuros.