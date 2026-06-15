from collections.abc import Iterable

from parsers.source.models.ExtractedSymbol import ExtractedSymbol
from llm.base import BaseEmbedding
from llm.factory import get_embedder
from llm.models import LLMEmbeddingRequest
from retrieval.embedding_builder import to_embedding_doc


def embed_symbol(
	symbol: ExtractedSymbol,
	*,
	embedder: BaseEmbedding
) -> dict:
	"""Create an embedding record for a single symbol."""
	text, metadata = to_embedding_doc(symbol)
	request = LLMEmbeddingRequest(
		input=text,
		model=embedder.model,
		label=symbol.qualified_name,
	)
	response = embedder.generate_embedding(request)

	return {
		"text": text,
		"metadata": metadata,
		"embedding": response.embedding,
		"model": response.model,
		"dimensions": response.dimensions,
	}


def embed_symbols(
	symbols: Iterable[ExtractedSymbol]
) -> list[dict]:
	"""Create embedding records for many symbols."""
	embedder = get_embedder()
	records: list[dict] = []
	for symbol in symbols:
		records.append(
			embed_symbol(symbol, embedder=embedder)
		)
	return records