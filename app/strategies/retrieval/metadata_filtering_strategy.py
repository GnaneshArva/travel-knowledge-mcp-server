"""Metadata Filtering Retrieval Strategy."""

from typing import Any, Dict, List, Optional
from app.dto.document import RetrievedDocumentDto
from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.interfaces.vectorstore_strategy import VectorStoreStrategy


class MetadataFilteringRetrievalStrategy(RetrievalStrategy):
    """Retrieval strategy that enforces strict pre-filtering on metadata fields (e.g., country, category)."""

    async def retrieve(
        self,
        processed_query: str,
        query_embedding: List[float],
        vector_store: VectorStoreStrategy,
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        # Ensure metadata_filter is populated
        active_filter = metadata_filter or {}

        # Perform pre-filtered vector search
        return await vector_store.search(
            query_embedding=query_embedding,
            limit=limit,
            metadata_filter=active_filter,
        )
