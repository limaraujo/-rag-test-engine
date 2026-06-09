from pydantic import BaseModel


class ExtractedSymbol(BaseModel):
    """
    Representa um símbolo extraído do código-fonte.

    Um "símbolo" aqui normalmente significa:
    - função
    - método
    - classe

    Esse objeto serve como unidade semântica para:
    - indexação vetorial
    - retrieval em RAG
    - geração de testes
    - análise estática
    """

    # Tipo do símbolo.
    #
    # Exemplos:
    # - "function"
    # - "method"
    # - "class"
    #
    # Útil para diferenciar:
    # função isolada:
    #     def foo()
    #
    # de método:
    #     class X:
    #         def foo()
    #
    symbol_type: str

    # Nome do símbolo.
    #
    # Exemplos:
    # - "create_user"
    # - "validate_token"
    # - "UserService"
    #
    # Serve como identificador principal.
    #
    name: str

    # Nome qualificado do símbolo.
    #
    # Exemplos:
    # - "create_user"
    # - "Calculadora.multiplica"
    # - "UserService.create"
    #
    # Evita colisões quando existem nomes iguais
    # em classes diferentes ou escopos distintos.
    #
    qualified_name: str

    # Nome da classe dona do símbolo.
    #
    # Será None para funções soltas.
    #
    # Exemplo:
    #
    # class UserService:
    #     def create():
    #
    # Resultado:
    # class_name = "UserService"
    #
    class_name: str | None

    # Caminho do arquivo original.
    #
    # Exemplo:
    # "src/services/user_service.py"
    #
    # Importante para:
    # - rastreabilidade
    # - navegação
    # - reconstrução de contexto
    #
    file_path: str

    # Código-fonte bruto do símbolo.
    #
    # Exemplo:
    #
    # def add(a, b):
    #     return a + b
    #
    # Esse é provavelmente o campo MAIS importante
    # para embeddings e geração de testes.
    #
    source_code: str

    # Lista de imports relevantes.
    #
    # Exemplos:
    # - "os"
    # - "typing.List"
    # - "services.user_service"
    #
    # Pode representar:
    # - imports do arquivo inteiro
    # - imports usados diretamente pela função
    #
    # Depende da estratégia adotada.
    #
    imports: list[str]

    # Dependências utilizadas pelo símbolo.
    #
    # Normalmente:
    # - funções chamadas
    # - métodos utilizados
    # - classes instanciadas
    #
    # Exemplos:
    # - "requests.get"
    # - "self.repo.save"
    # - "User"
    #
    # Muito útil para:
    # - entender acoplamento
    # - inferir mocks necessários
    # - gerar testes automaticamente
    #
    dependencies: list[str]

    # Exceptions relacionadas ao símbolo.
    #
    # Pode incluir:
    # - exceptions lançadas (raise)
    # - exceptions capturadas (except)
    #
    # Exemplos:
    # - "ValueError"
    # - "HTTPException(404)"
    #
    # Importante para geração de testes negativos.
    #
    exceptions: list[str]

    # Decorators aplicados ao símbolo.
    #
    # Exemplos:
    # - "@staticmethod"
    # - "@cache"
    # - "@router.get('/users')"
    #
    # Decorators alteram comportamento semântico,
    # então ignorá-los costuma gerar contexto incompleto.
    #
    decorators: list[str]

    # Docstring oficial do símbolo.
    #
    # Exemplo:
    #
    # def foo():
    #     '''
    #     Faz autenticação do usuário.
    #     '''
    #
    # Pode ser None caso não exista.
    #
    # Frequentemente útil para RAG,
    # porque docstrings tendem a conter
    # intenção semântica explícita.
    #
    docstring: str | None

    # Quantidade de desvios de fluxo ("branches").
    #
    # Normalmente conta:
    # - if
    # - elif
    # - for
    # - while
    # - try
    # - match
    #
    # Serve como aproximação simples
    # de complexidade ciclomática.
    #
    # Quanto maior:
    # - maior dificuldade de teste
    # - maior número de cenários
    #
    branches: int

    # Lista heurística de edge cases inferidos.
    #
    # Exemplos:
    # - "division_by_zero"
    # - "null_input"
    # - "empty_list"
    # - "index_out_of_bounds"
    #
    # Isso NÃO vem diretamente da AST.
    # É inferido por regras heurísticas.
    #
    # Campo extremamente útil para LLMs
    # gerarem testes mais inteligentes.
    #
    edge_cases: list[str]