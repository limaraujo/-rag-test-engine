from __future__ import annotations

import logging
from pathlib import Path

from ingest.call_graph import CallGraph
from ingest.dependency_graph import DependencyGraph
from ingest.import_resolver import module_name_from_path
from ingest.models.ExtractedSymbol import ExtractedSymbol
from llm.base import BaseEmbedding
from llm.factory import get_embedder
from llm.models import LLMEmbeddingRequest
from retrieval.embedding_builder import content_hash, to_embedding_doc
from retrieval.hybrid import HybridCandidate, rerank_candidates
from retrieval.qdrant_client import QdrantStore
from schemas.context import FunctionContext
from schemas.retrieval_context import RetrievalContext, RetrievalMetrics

from config.settings import settings

logger = logging.getLogger(__name__)


class Retriever:
    """
    Enriquece um :class:`~schemas.context.FunctionContext` com contexto RAG híbrido.

    Dado um símbolo, o retriever:

    1. Constrói a representação textual canônica (mesmo formato utilizado
       durante a indexação — garante que os vetores da consulta e os vetores
       armazenados estejam no mesmo espaço semântico).
    2. Gera embeddings do texto utilizando o modelo configurado.
    3. Pesquisa na coleção **symbols** por funções semanticamente semelhantes.
    4. Enriquece com vizinhos do **call graph** (callers/callees) e do
       **dependency graph** (módulos/classes dependentes).
    5. Reordena candidatos com score híbrido::

           score = 0.5 * vector_similarity
                 + 0.3 * dependency_score
                 + 0.2 * call_graph_score

    6. Pesquisa na coleção **tests** por arquivos de teste semelhantes.
    7. Retorna um novo ``FunctionContext`` com :class:`RetrievalContext`
       preenchido (limites configuráveis em ``related_functions`` e ``similar_tests``).

    As duas coleções são independentes:

    * ``settings.QDRANT_COLLECTION_SYMBOLS`` (padrão: ``"symbols"``)
      Símbolos de código de produção indexados por :meth:`index_symbols`.

    * ``settings.QDRANT_COLLECTION_TESTS`` (padrão: ``"tests"``)
      Código de testes existente indexado por :meth:`index_tests`.

    Se alguma das coleções estiver vazia ou ainda não tiver sido criada,
    o campo RAG correspondente permanece como uma lista vazia — o pipeline
    degrada de forma graciosa para o fluxo sem RAG.
    """

    def __init__(
        self,
        store: QdrantStore | None = None,
        embedder: BaseEmbedding | None = None,
    ) -> None:
        self._store = store or QdrantStore()
        self._embedder = embedder or get_embedder()

    # ──────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────

    def enrich(
        self,
        ctx: FunctionContext,
        symbol: ExtractedSymbol,
        *,
        call_graph: CallGraph | None = None,
        dependency_graph: DependencyGraph | None = None,
        symbols_by_name: dict[str, ExtractedSymbol] | None = None,
        project_root: str | Path | None = None,
        top_k: int | None = None,
        top_k_functions: int | None = None,
        top_k_tests: int | None = None,
        score_threshold: float | None = None,
    ) -> FunctionContext:
        """
        Retorna uma cópia de *ctx* com contexto RAG híbrido preenchido.

        O *ctx* original nunca é modificado (é utilizado o
        ``model_copy`` do Pydantic).
        """
        limit = top_k_functions or top_k or settings.RETRIEVER_TOP_K_FUNCTIONS
        k_tests = top_k_tests or settings.RETRIEVER_TOP_K_TESTS
        threshold = (
            score_threshold
            if score_threshold is not None
            else settings.RETRIEVER_SCORE_THRESHOLD
        )

        query_vector = self._embed(symbol)
        symbols_index = symbols_by_name or {}

        caller_qnames, callee_qnames, dependency_qnames = self._graph_qualified_names(
            symbol,
            call_graph=call_graph,
            dependency_graph=dependency_graph,
            symbols_by_name=symbols_index,
            project_root=project_root,
        )

        caller_functions = self._source_texts(caller_qnames, symbols_index)
        callee_functions = self._source_texts(callee_qnames, symbols_index)
        dependency_functions = self._source_texts(dependency_qnames, symbols_index)

        vector_hits = self._search_symbols(
            query_vector,
            exclude_name=symbol.qualified_name,
            top_k=settings.RETRIEVER_RERANK_POOL_SIZE,
            score_threshold=threshold,
        )

        related = self._hybrid_rerank(
            vector_hits=vector_hits,
            dependency_qnames=dependency_qnames,
            caller_qnames=caller_qnames,
            callee_qnames=callee_qnames,
            symbols_by_name=symbols_index,
            top_k=limit,
        )

        similar_tests = self._fetch_similar_tests(
            query_vector,
            top_k=k_tests,
            score_threshold=threshold,
        )

        retrieval_context = RetrievalContext(
            related_functions=related,
            dependency_functions=dependency_functions,
            caller_functions=caller_functions,
            callee_functions=callee_functions,
            similar_tests=similar_tests,
        )

        metrics = RetrievalMetrics(
            qualified_name=symbol.qualified_name,
            vector_candidates=len(vector_hits),
            dependency_neighbors=len(dependency_qnames),
            call_graph_neighbors=len(caller_qnames) + len(callee_qnames),
            reranked_candidates=len(related),
            top_hybrid_score=self._last_top_score,
            avg_hybrid_score=self._last_avg_score,
            similar_tests_count=len(similar_tests),
        )
        logger.info(metrics.log_summary())

        return ctx.model_copy(
            update={
                "retrieval_context": retrieval_context,
                "related_functions": related,
                "similar_tests": similar_tests,
            }
        )

    def index_symbols(
        self,
        symbols: list[ExtractedSymbol],
        *,
        batch_size: int = 32,
        force: bool | None = None,
    ) -> tuple[int, int]:
        """
        Gera embeddings e realiza upsert dos símbolos na coleção de símbolos.

        Retorna (indexados, ignorados). Com ``force=False`` (padrão via
        ``settings.REINDEX_SYMBOLS``), símbolos já no Qdrant com o mesmo
        conteúdo são pulados.
        """
        from retrieval.embeddings import embed_symbol

        reindex = settings.REINDEX_SYMBOLS if force is None else force
        collection = settings.QDRANT_COLLECTION_SYMBOLS
        batch: list[dict] = []
        indexed = 0
        skipped = 0

        for symbol in symbols:
            text, metadata = to_embedding_doc(symbol)
            digest = content_hash(text)

            if not reindex:
                cached = self._store.get_vector(collection, symbol.qualified_name)
                if cached and cached[1].get("content_hash") == digest:
                    skipped += 1
                    continue

            record = embed_symbol(symbol, embedder=self._embedder)
            record["metadata"]["content_hash"] = digest
            batch.append(record)

            if len(batch) >= batch_size:
                self._store.upsert(collection, batch)
                indexed += len(batch)
                batch.clear()

        if batch:
            self._store.upsert(collection, batch)
            indexed += len(batch)

        return indexed, skipped

    def index_tests(
        self,
        test_records: list[dict],
        *,
        batch_size: int = 32,
    ) -> int:
        """Realiza upsert de registros de embeddings de testes na coleção de testes."""
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

    _last_top_score: float = 0.0
    _last_avg_score: float = 0.0

    def _embed(self, symbol: ExtractedSymbol) -> list[float]:
        text, _ = to_embedding_doc(symbol)
        digest = content_hash(text)
        collection = settings.QDRANT_COLLECTION_SYMBOLS

        cached = self._store.get_vector(collection, symbol.qualified_name)
        if cached and cached[1].get("content_hash") == digest:
            return cached[0]

        request = LLMEmbeddingRequest(
            input=text,
            model=self._embedder.model,
            label=symbol.qualified_name,
        )
        response = self._embedder.generate_embedding(request)
        return response.embedding

    def _search_symbols(
        self,
        query_vector: list[float],
        *,
        exclude_name: str,
        top_k: int,
        score_threshold: float,
    ) -> dict[str, tuple[str, float]]:
        """Retorna mapa qualified_name → (text, vector_similarity)."""
        collection = settings.QDRANT_COLLECTION_SYMBOLS
        if not self._store.collection_exists(collection):
            return {}

        hits = self._store.search(
            collection,
            query_vector,
            top_k=top_k + 1,
            score_threshold=score_threshold,
        )

        results: dict[str, tuple[str, float]] = {}
        for hit in hits:
            payload = hit.payload or {}
            qname = payload.get("qualified_name", "")
            if not qname or qname == exclude_name:
                continue
            text = payload.get("text", "").strip()
            if text:
                results[qname] = (text, float(hit.score))
            if len(results) >= top_k:
                break

        return results

    def _graph_qualified_names(
        self,
        symbol: ExtractedSymbol,
        *,
        call_graph: CallGraph | None,
        dependency_graph: DependencyGraph | None,
        symbols_by_name: dict[str, ExtractedSymbol],
        project_root: str | Path | None,
    ) -> tuple[set[str], set[str], set[str]]:
        caller_qnames: set[str] = set()
        callee_qnames: set[str] = set()
        dependency_qnames: set[str] = set()

        if call_graph is not None:
            node = call_graph.nodes.get(symbol.qualified_name)
            if node is not None:
                caller_qnames = {
                    name for name in node.called_by if name in symbols_by_name
                }
                callee_qnames = {
                    name for name in node.calls if name in symbols_by_name
                }

        if dependency_graph is not None and project_root is not None:
            root = Path(project_root).resolve()
            module_name = module_name_from_path(root, Path(symbol.file_path))
            dep_entities: set[str] = set()

            module_node = dependency_graph.nodes.get(module_name)
            if module_node is not None:
                dep_entities.update(module_node.dependencies)

            if symbol.class_name:
                class_key = f"{module_name}.{symbol.class_name}"
                class_node = dependency_graph.nodes.get(class_key)
                if class_node is not None:
                    dep_entities.update(class_node.dependencies)

            dependency_qnames = self._symbols_for_dependency_entities(
                dep_entities,
                symbols_by_name=symbols_by_name,
                project_root=root,
            )

        return caller_qnames, callee_qnames, dependency_qnames

    def _symbols_for_dependency_entities(
        self,
        entities: set[str],
        *,
        symbols_by_name: dict[str, ExtractedSymbol],
        project_root: Path,
    ) -> set[str]:
        matched: set[str] = set()

        for entity in entities:
            if entity in symbols_by_name:
                matched.add(entity)
                continue

            for qname, sym in symbols_by_name.items():
                module_name = module_name_from_path(project_root, Path(sym.file_path))
                if sym.class_name:
                    class_key = f"{module_name}.{sym.class_name}"
                    if entity == class_key or entity == module_name:
                        matched.add(qname)
                elif entity == module_name:
                    matched.add(qname)

        return matched

    def _hybrid_rerank(
        self,
        *,
        vector_hits: dict[str, tuple[str, float]],
        dependency_qnames: set[str],
        caller_qnames: set[str],
        callee_qnames: set[str],
        symbols_by_name: dict[str, ExtractedSymbol],
        top_k: int,
    ) -> list[str]:
        all_qnames = (
            set(vector_hits)
            | dependency_qnames
            | caller_qnames
            | callee_qnames
        )

        candidates: list[HybridCandidate] = []
        for qname in all_qnames:
            if qname in symbols_by_name:
                text = symbols_by_name[qname].source_code.strip()
                vector_sim = vector_hits[qname][1] if qname in vector_hits else 0.0
            elif qname in vector_hits:
                text, vector_sim = vector_hits[qname]
            else:
                continue

            if not text:
                continue

            candidates.append(
                HybridCandidate(
                    qualified_name=qname,
                    text=text,
                    vector_similarity=vector_sim,
                    dependency_score=1.0 if qname in dependency_qnames else 0.0,
                    call_graph_score=(
                        1.0
                        if qname in caller_qnames or qname in callee_qnames
                        else 0.0
                    ),
                )
            )

        ranked = rerank_candidates(candidates, top_k=top_k)
        scores = [c.hybrid_score for c in ranked]
        self._last_top_score = scores[0] if scores else 0.0
        self._last_avg_score = sum(scores) / len(scores) if scores else 0.0

        return [f"symbol: {c.qualified_name}\n{c.text}" for c in ranked]

    def _source_texts(
        self,
        qualified_names: set[str],
        symbols_by_name: dict[str, ExtractedSymbol],
    ) -> list[str]:
        texts: list[str] = []
        for qname in sorted(qualified_names):
            symbol = symbols_by_name.get(qname)
            if symbol is None:
                continue
            code = symbol.source_code.strip()
            if code:
                texts.append(f"symbol: {qname}\n{code}")
        return texts

    def _fetch_similar_tests(
        self,
        query_vector: list[float],
        *,
        top_k: int,
        score_threshold: float,
    ) -> list[str]:
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
