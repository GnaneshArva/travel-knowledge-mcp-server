"""Hybrid Retrieval Strategy (BM25 Keyword + Dense Vector Search with Reciprocal Rank Fusion)."""

from typing import Any, Dict, List, Optional
import math
from app.dto.document import RetrievedDocumentDto
from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.interfaces.vectorstore_strategy import VectorStoreStrategy


class HybridRetrievalStrategy(RetrievalStrategy):
    """Combines BM25 lexical keyword matching with dense vector similarity search using Reciprocal Rank Fusion (RRF)."""

    def __init__(self, rrf_k: int = 60, alpha: float = 0.5):
        self.rrf_k = rrf_k
        self.alpha = alpha  # Weight balance between vector and BM25

    def _simple_bm25_score(self, query: str, text: str) -> float:
        """Calculates basic BM25 keyword frequency score."""
        query_words = set(query.lower().split())
        text_words = text.lower().split()
        if not text_words:
            return 0.0
        
        score = 0.0
        for word in query_words:
            count = text_words.count(word)
            if count > 0:
                tf = count / len(text_words)
                score += (tf * (1.5 + 1)) / (tf + 1.5)
        return score

    async def retrieve(
        self,
        processed_query: str,
        query_embedding: List[float],
        vector_store: VectorStoreStrategy,
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        # 1. Retrieve candidates using dense vector similarity (fetch double limit)
        vector_candidates = await vector_store.search(
            query_embedding=query_embedding,
            limit=limit * 2,
            metadata_filter=metadata_filter,
        )

        if not vector_candidates:
            return []

        # 2. Score candidates using BM25 keyword matching
        bm25_scored = []
        for doc in vector_candidates:
            bm25_score = self._simple_bm25_score(processed_query, doc.content)
            bm25_scored.append((doc, bm25_score))

        bm25_sorted = sorted(bm25_scored, key=lambda x: x[1], reverse=True)

        # 3. Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[str, float] = {}
        doc_map: Dict[str, RetrievedDocumentDto] = {}

        # Vector ranks
        for rank, doc in enumerate(vector_candidates):
            doc_map[doc.id] = doc
            rrf_scores[doc.id] = rrf_scores.get(doc.id, 0.0) + self.alpha * (1.0 / (self.rrf_k + rank + 1))

        # BM25 ranks
        for rank, (doc, _) in enumerate(bm25_sorted):
            rrf_scores[doc.id] = rrf_scores.get(doc.id, 0.0) + (1.0 - self.alpha) * (1.0 / (self.rrf_k + rank + 1))

        # Sort by final RRF score
        fused_docs = sorted(doc_map.values(), key=lambda d: rrf_scores.get(d.id, 0.0), reverse=True)

        return fused_docs[:limit]
