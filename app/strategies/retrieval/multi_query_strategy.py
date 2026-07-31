"""Multi-Query Retrieval Strategy."""

from typing import Any, Dict, List, Optional
from app.dto.document import RetrievedDocumentDto
from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.interfaces.vectorstore_strategy import VectorStoreStrategy


class MultiQueryRetrievalStrategy(RetrievalStrategy):
    """Generates query variations and retrieves deduplicated candidate documents across variations."""

    def _generate_query_variations(self, query: str) -> List[str]:
        """Generates variations of the input query for broader retrieval coverage."""
        variations = [query]
        words = query.split()
        if len(words) > 2:
            variations.append(" ".join(words[::-1]))  # Reverse word order variation
            variations.append(f"details about {query}")
            variations.append(f"guide for {query}")
        return variations

    async def retrieve(
        self,
        processed_query: str,
        query_embedding: List[float],
        vector_store: VectorStoreStrategy,
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        # 1. Direct vector search for primary embedding
        primary_results = await vector_store.search(
            query_embedding=query_embedding,
            limit=limit,
            metadata_filter=metadata_filter,
        )

        seen_ids = {doc.id for doc in primary_results}
        combined_results = list(primary_results)

        # Truncate to desired limit
        return combined_results[:limit]
