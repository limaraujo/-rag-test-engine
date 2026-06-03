from __future__ import annotations
 
from ingest.models.ExtractedSymbol import ExtractedSymbol
from llm.gemini_embedding import GeminiEmbedding
from llm.models import LLMEmbeddingRequest
from retrieval.embedding_builder import to_embedding_doc
from retrieval.qdrant_client import QdrantStore
from schemas.context import FunctionContext
 
from config.settings import settings
 
 
class Retriever:
    """
    Enriquece um :class:`~schemas.context.FunctionContext` com contexto RAG.

    Dado um símbolo, o retriever:

    1. Constrói a representação textual canônica (mesmo formato utilizado
       durante a indexação — garante que os vetores da consulta e os vetores
       armazenados estejam no mesmo espaço semântico).
    2. Gera embeddings do texto utilizando o modelo configurado.
    3. Pesquisa na coleção **symbols** por funções e métodos semanticamente
       semelhantes presentes no código.
    4. Pesquisa na coleção **tests** por arquivos de teste semelhantes.
    5. Retorna um novo ``FunctionContext`` com ``related_functions`` e
       ``similar_tests`` preenchidos.

    As duas coleções são independentes:

    * ``settings.QDRANT_COLLECTION_SYMBOLS`` (padrão: ``"symbols"``)
      Símbolos de código de produção indexados por :meth:`index_symbols`.

    * ``settings.QDRANT_COLLECTION_TESTS`` (padrão: ``"tests"``)
      Código de testes existente indexado por :meth:`index_tests`.

    Se alguma das coleções estiver vazia ou ainda não tiver sido criada,
    o campo RAG correspondente permanece como uma lista vazia — o pipeline
    degrada de forma graciosa para o fluxo sem RAG.

    Exemplo rápido
    --------------
    ::

        from ingest.parser import parse_repository_symbols
        from retrieval.retriever import Retriever
        from schemas.context import FunctionContext

        retriever = Retriever()

        # --- indexação única (faça isso antes de gerar testes) ---
        symbols = parse_repository_symbols("src/")
        retriever.index_symbols(symbols)

        # --- enriquecimento por função ---
        for symbol in symbols:
            ctx = FunctionContext.from_symbol(symbol)
            ctx = retriever.enrich(ctx, symbol)
            # ctx.related_functions e ctx.similar_tests agora estão preenchidos
    """
 
    def __init__(
        self,
        store: QdrantStore | None = None,
        embedder: GeminiEmbedding | None = None,
    ) -> None:
        self._store = store or QdrantStore()
        self._embedder = embedder or GeminiEmbedding()
 
    # ──────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────
 
    def enrich(
        self,
        ctx: FunctionContext,
        symbol: ExtractedSymbol,
        *,
        top_k_functions: int | None = None,
        top_k_tests: int | None = None,
        score_threshold: float | None = None,
    ) -> FunctionContext:
        """
        Retorna uma cópia de *ctx* com ``related_functions`` e
        ``similar_tests`` preenchidos a partir do Qdrant.

        O *ctx* original nunca é modificado (é utilizado o
        ``model_copy`` do Pydantic).

        Args:
            ctx:              Contexto construído a partir de *symbol* —
                              os demais campos já estão preenchidos;
                              este método apenas preenche os dois
                              campos RAG.
            symbol:           O :class:`~ingest.models.ExtractedSymbol`
                              que está sendo enriquecido. É utilizado para
                              construir o vetor de consulta e excluir o
                              próprio símbolo dos resultados.
            top_k_functions:  Quantidade de trechos de funções relacionadas
                              a recuperar. Padrão:
                              ``settings.RETRIEVER_TOP_K_FUNCTIONS``.
            top_k_tests:      Quantidade de trechos de testes semelhantes
                              a recuperar. Padrão:
                              ``settings.RETRIEVER_TOP_K_TESTS``.
            score_threshold:  Similaridade cosseno mínima (0 – 1) para que
                              um resultado seja incluído. Padrão:
                              ``settings.RETRIEVER_SCORE_THRESHOLD``.

        Returns:
            Uma nova instância de ``FunctionContext`` com os campos RAG
            preenchidos.
        """

        k_funcs = top_k_functions or settings.RETRIEVER_TOP_K_FUNCTIONS
        k_tests = top_k_tests or settings.RETRIEVER_TOP_K_TESTS
        threshold = score_threshold if score_threshold is not None \
            else settings.RETRIEVER_SCORE_THRESHOLD
 
        query_vector = self._embed(symbol)
 
        related = self._fetch_related_functions(
            query_vector,
            exclude_name=symbol.qualified_name,
            top_k=k_funcs,
            score_threshold=threshold,
        )
 
        similar_tests = self._fetch_similar_tests(
            query_vector,
            top_k=k_tests,
            score_threshold=threshold,
        )
 
        return ctx.model_copy(
            update={
                "related_functions": related,
                "similar_tests": similar_tests,
            }
        )
 
    def index_symbols(
        self,
        symbols: list[ExtractedSymbol],
        *,
        batch_size: int = 32,
    ) -> int:
        """
        Gera embeddings e realiza upsert dos símbolos de código de produção
        na coleção de símbolos.

        Pode ser chamado várias vezes com segurança — registros existentes
        são sobrescritos (semântica de upsert, utilizando
        ``qualified_name`` como chave).

        Args:
            symbols:    Símbolos extraídos por
                        :func:`~ingest.parser.parse_repository_symbols`.
            batch_size: Quantidade de embeddings por chamada de upsert
                        ao Qdrant. Reduza esse valor caso encontre
                        limites de taxa (rate limits).

        Returns:
            Número total de registros inseridos/atualizados.
        """
        from retrieval.embeddings import embed_symbol
 
        collection = settings.QDRANT_COLLECTION_SYMBOLS
        batch: list[dict] = []
        total = 0
 
        for symbol in symbols:
            batch.append(embed_symbol(symbol, embedder=self._embedder))
            if len(batch) >= batch_size:
                self._store.upsert(collection, batch)
                total += len(batch)
                batch.clear()
 
        if batch:
            self._store.upsert(collection, batch)
            total += len(batch)
 
        return total
 
    def index_tests(
        self,
        test_records: list[dict],
        *,
        batch_size: int = 32,
    ) -> int:
        """
        Realiza upsert de registros de embeddings de testes previamente
        construídos na coleção de testes.

        Os registros de teste possuem o mesmo formato dos produzidos por
        :func:`~retrieval.embeddings.embed_symbol`. Eles podem ser criados
        tratando cada função de teste como um ``ExtractedSymbol`` e
        chamando ``embed_symbols``, ou construídos manualmente.

        Formato esperado::

            {
                "text":       str,           # código do teste (ou descrição)
                "metadata":   {
                    "qualified_name": str,   # ID único, ex.: "test_divide_by_zero"
                    "symbol_type":    str,   # "test_function"
                    "class_name":     str | None,
                    "file_path":      str,
                },
                "embedding":  list[float],
                "model":      str,
                "dimensions": int,
            }

        Args:
            test_records: Registros de teste já embutidos (embedded).
            batch_size:   Quantidade de registros por chamada de upsert.

        Returns:
            Número total de registros inseridos/atualizados.
        """
        collection = settings.QDRANT_COLLECTION_TESTS
        total = 0
 
        for i in range(0, len(test_records), batch_size):
            batch = test_records[i : i + batch_size]
            self._store.upsert(collection, batch)
            total += len(batch)
 
        return total
 
    # ──────────────────────────────────────────────────────────────────
    # Internal helpers
    # ──────────────────────────────────────────────────────────────────
 
    def _embed(self, symbol: ExtractedSymbol) -> list[float]:
        """
        Produz o vetor de consulta para um símbolo.

        Utiliza o mesmo formato textual empregado durante a indexação,
        garantindo que os vetores de consulta e os vetores armazenados
        estejam no mesmo espaço semântico.
        """
        text, _ = to_embedding_doc(symbol)
        request = LLMEmbeddingRequest(
            input=text,
            model=self._embedder.model,
        )
        response = self._embedder.generate_embedding(request)
        return response.embedding
 
    def _fetch_related_functions(
        self,
        query_vector: list[float],
        *,
        exclude_name: str,
        top_k: int,
        score_threshold: float,
    ) -> list[str]:
        """
        Pesquisa na coleção de símbolos e retorna o campo ``text`` de cada
        resultado encontrado, excluindo o próprio símbolo.

        Solicitamos ``top_k + 1`` resultados para absorver o auto-match
        (o símbolo sendo enriquecido quase certamente será o resultado mais
        próximo de si mesmo).
        """
        collection = settings.QDRANT_COLLECTION_SYMBOLS
        if not self._store.collection_exists(collection):
            return []
 
        hits = self._store.search(
            collection,
            query_vector,
            top_k=top_k + 1,
            score_threshold=score_threshold,
        )
 
        results: list[str] = []
        for hit in hits:
            payload = hit.payload or {}
            if payload.get("qualified_name") == exclude_name:
                continue
            text = payload.get("text", "").strip()
            if text:
                results.append(text)
            if len(results) >= top_k:
                break
 
        return results
 
    def _fetch_similar_tests(
        self,
        query_vector: list[float],
        *,
        top_k: int,
        score_threshold: float,
    ) -> list[str]:
        """
        Pesquisa na coleção de testes e retorna o campo ``text`` de cada
        resultado encontrado.
        """
        collection = settings.QDRANT_COLLECTION_TESTS
        if not self._store.collection_exists(collection):
            return []
 
        hits = self._store.search(
            collection,
            query_vector,
            top_k=top_k,
            score_threshold=score_threshold,
        )
 
        return [
            hit.payload.get("text", "").strip()
            for hit in hits
            if hit.payload and hit.payload.get("text", "").strip()
        ]
