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
  title: [Integração de Análise Estática e Retrieval-Augmented Generation para Geração de Testes Unitários com LLMs],
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
