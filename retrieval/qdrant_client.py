from __future__ import annotations
 
import uuid
from typing import Any
 
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    ScoredPoint,
    VectorParams,
)
 
from config.settings import settings
 
 
# Namespace determinístico para a geração de UUID-5.
# Alterar isto invalida todos os IDs armazenados anteriormente.
_UUID_NAMESPACE = uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
 
 
def _point_id(qualified_name: str) -> str:
    """
    Deriva um UUID estável a partir do nome qualificado de um símbolo.
 
    O uso do uuid5 significa que fazer o upsert do mesmo símbolo duas vezes
    sempre resultará no mesmo ponto — sem duplicatas, mesmo se o job de indexação
    for executado novamente.
    """
    return str(uuid.uuid5(_UUID_NAMESPACE, qualified_name))
 
 
class QdrantStore:
    """
    Wrapper leve e opinativo para o qdrant-client oficial.
 
    Responsabilidades
    ----------------
    - Gerenciamento de conexão (local em memória, local em disco ou nuvem remota).
    - Bootstrap idempotente de coleção — seguro para ser chamado em cada inicialização.
    - Upsert de registros de embeddings produzidos por ``retrieval.embeddings``.
    - Busca de similaridade ANN com filtros opcionais de payload.
 
    Modos de conexão
    ----------------
    Controlado por ``settings.QDRANT_URL``:
 
    * ``:memory:``
        No próprio processo, efêmero. Ideal para testes unitários e CI.
        Nenhum servidor é necessário; os dados são perdidos quando o processo termina.
 
    * ``http://localhost:6333`` (padrão)
        Servidor Qdrant local iniciado via Docker ou binário nativo.
 
    * ``https://<cluster>.cloud.qdrant.io``
        Qdrant Cloud. Usar em conjunto com ``settings.QDRANT_API_KEY``.
 
    Exemplo
    -------
    ::
 
        store = QdrantStore()
        store.upsert("symbols", records)
        hits = store.search("symbols", query_vector, top_k=5)
    """
 
    def __init__(self) -> None:
        if settings.QDRANT_URL == ":memory:":
            self._client: QdrantClient = QdrantClient(":memory:")
        else:
            self._client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY or None,
            )
 
    # ──────────────────────────────────────────────────────────────────
    # Gerenciamento de coleções
    # ──────────────────────────────────────────────────────────────────
 
    def ensure_collection(
        self,
        name: str,
        *,
        vector_size: int | None = None,
        distance: Distance = Distance.COSINE,
    ) -> None:
        """
        Cria ``name`` se ainda não existir.
 
        Idempotente — chamar isso várias vezes é seguro.
 
        Args:
            name:        Nome da coleção.
            vector_size: Dimensões do embedding. Usa o valor de
                         ``settings.EMBEDDING_DIMENSIONS`` como fallback quando omitido.
            distance:    Métrica de similaridade. O padrão é cosseno.
        """
        size = vector_size or settings.EMBEDDING_DIMENSIONS
        existing = {c.name for c in self._client.get_collections().collections}
        if name not in existing:
            self._client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=size, distance=distance),
            )
 
    def collection_exists(self, name: str) -> bool:
        """Retorna True se a coleção foi criada."""
        return name in {
            c.name for c in self._client.get_collections().collections
        }
 
    def count(self, name: str) -> int:
        """Retorna o número de pontos armazenados em ``name``."""
        result = self._client.count(collection_name=name, exact=True)
        return result.count
 
    def delete_collection(self, name: str) -> None:
        """
        Exclui uma coleção inteiramente.
 
        Útil ao reindexar do zero:
        ``store.delete_collection("symbols")``
        ``store.upsert("symbols", fresh_records)``
        """
        self._client.delete_collection(name)
 
    # ──────────────────────────────────────────────────────────────────
    # Escrita
    # ──────────────────────────────────────────────────────────────────
 
    def upsert(
        self,
        collection_name: str,
        records: list[dict[str, Any]],
    ) -> None:
        """
        Faz o upsert de um lote de registros de embeddings em ``collection_name``.
 
        A coleção é criada automaticamente no primeiro upsert se ela
        ainda não existir — não há necessidade de chamar ``ensure_collection`` manualmente.
 
        Formato esperado do registro (corresponde a ``retrieval.embeddings.embed_symbol``)::
 
            {
                "text":       str,           # texto completo que foi transformado em embedding
                "metadata":   {              # proveniente do embedding_builder
                    "qualified_name": str,
                    "symbol_type":    str,
                    "class_name":     str | None,
                    "file_path":      str,
                },
                "embedding":  list[float],   # vetor produzido pelo modelo de embedding
                "model":      str,           # identificador do modelo (para rastreabilidade)
                "dimensions": int,           # len(embedding)
            }
 
        Args:
            collection_name: Coleção de destino.
            records:         Lista não vazia de registros de embeddings.
        """
        if not records:
            return
 
        self.ensure_collection(
            collection_name,
            vector_size=records[0]["dimensions"],
        )
 
        points = [
            PointStruct(
                id=_point_id(r["metadata"]["qualified_name"]),
                vector=r["embedding"],
                payload={
                    **r["metadata"],
                    "text": r["text"],
                    "model": r["model"],
                },
            )
            for r in records
        ]
 
        self._client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True,   # bloqueia até que a escrita seja persistida
        )
 
    # ──────────────────────────────────────────────────────────────────
    # Busca
    # ──────────────────────────────────────────────────────────────────
 
    def search(
        self,
        collection_name: str,
        query_vector: list[float],
        *,
        top_k: int = 5,
        score_threshold: float | None = None,
        filter_by: dict[str, Any] | None = None,
    ) -> list[ScoredPoint]:
        """
        Busca aproximada de vizinhos mais próximos (ANN).
 
        Args:
            collection_name: Coleção de destino.
            query_vector:    Embedding do símbolo de busca.
            top_k:           Número máximo de resultados a retornar.
            score_threshold: Similaridade de cosseno mínima (0 – 1). ``None``
                             significa sem limite — retorna o top-k independentemente
                             do score.
            filter_by:       Dicionário opcional de filtros chave → valor do payload
                             aplicados como condições AND. Exemplo::
 
                                 {"symbol_type": "function"}
 
        Returns:
            Lista de :class:`~qdrant_client.models.ScoredPoint` ordenada de forma
            descendente pelo score de similaridade. Cada ponto carrega um dicionário
            ``payload`` que inclui ``"text"``, ``"qualified_name"``, etc.
        """
        qdrant_filter: Filter | None = None
        if filter_by:
            qdrant_filter = Filter(
                must=[
                    FieldCondition(key=k, match=MatchValue(value=v))
                    for k, v in filter_by.items()
                ]
            )
 
        return self._client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
            query_filter=qdrant_filter,
            with_payload=True,
            with_vectors=False,
        )