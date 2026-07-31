"""Agentic Adaptive Retrieval Strategy."""

from typing import Any, Dict, List, Optional
from app.dto.document import RetrievedDocumentDto
from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.interfaces.vectorstore_strategy import VectorStoreStrategy


class AgenticRetrievalStrategy(RetrievalStrategy):
    """Adaptive multi-step retrieval strategy that iteratively searches and adjusts filters based on initial score quality."""

    async def retrieve(
        self,
        processed_query: str,
        query_embedding: List[float],
        vector_store: VectorStoreStrategy,
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        # Step 1: Initial restricted search with metadata filter
        results = await vector_store.search(
            query_embedding=query_embedding,
            limit=limit,
            metadata_filter=metadata_filter,
        )

        # Step 2: Adaptive expansion — if results are insufficient, fallback without strict filter
        if len(results) < limit:
            fallback_results = await vector_store.search(
                query_embedding=query_embedding,
                limit=limit,
                metadata_filter=None,
            )
            seen = {d.id for d in results}
            for doc in fallback_results:
                if doc.id not in seen:
                    results.append(doc)
                    seen.add(doc.id)
                if len(results) >= limit:
                    break

        return results[:limit]
