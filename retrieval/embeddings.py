from collections.abc import Iterable

from ingest.models.ExtractedSymbol import ExtractedSymbol
from llm.gemini_embedding import GeminiEmbedding
from llm.models import LLMEmbeddingRequest
from retrieval.embedding_builder import to_embedding_doc


def embed_symbol(
	symbol: ExtractedSymbol,
	*,
	embedder: GeminiEmbedding
) -> dict:
	"""Create an embedding record for a single symbol."""
	text, metadata = to_embedding_doc(symbol)
	request = LLMEmbeddingRequest(
		input=text,
		model=embedder.model
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
	"""Create embedding records for many symbols using Gemini."""
	embedder = GeminiEmbedding()
	records: list[dict] = []
	for symbol in symbols:
		records.append(
			embed_symbol(symbol, embedder=embedder)
		)
	return records