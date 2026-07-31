"""Contextual Compression Retrieval Strategy."""

from typing import Any, Dict, List, Optional
import re
from app.dto.document import RetrievedDocumentDto
from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.interfaces.vectorstore_strategy import VectorStoreStrategy


class ContextualCompressionRetrievalStrategy(RetrievalStrategy):
    """Trims and extracts relevant sentences from candidate chunks to reduce prompt noise."""

    def _compress_content(self, query: str, content: str) -> str:
        query_words = set(query.lower().split())
        sentences = re.split(r"(?<=[.!?])\s+", content)

        relevant_sentences = []
        for s in sentences:
            s_words = set(s.lower().split())
            if query_words.intersection(s_words):
                relevant_sentences.append(s)

        return " ".join(relevant_sentences) if relevant_sentences else content

    async def retrieve(
        self,
        processed_query: str,
        query_embedding: List[float],
        vector_store: VectorStoreStrategy,
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        raw_candidates = await vector_store.search(
            query_embedding=query_embedding,
            limit=limit,
            metadata_filter=metadata_filter,
        )

        compressed_docs = []
        for doc in raw_candidates:
            compressed_text = self._compress_content(processed_query, doc.content)
            compressed_docs.append(
                RetrievedDocumentDto(
                    id=doc.id,
                    content=compressed_text,
                    similarity_score=doc.similarity_score,
                    metadata=doc.metadata,
                )
            )

        return compressed_docs
