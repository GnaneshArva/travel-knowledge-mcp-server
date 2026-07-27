"""Vector Similarity Retrieval Strategy implementation."""

from typing import Any, Dict, List, Optional
from app.dto.document import RetrievedDocumentDto
from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.interfaces.vectorstore_strategy import VectorStoreStrategy


class VectorSimilarityRetrievalStrategy(RetrievalStrategy):
    """Retrieval strategy executing semantic vector similarity search via VectorStoreStrategy.

    Decoupled from specific vector store vendors or APIs.
    """

    async def retrieve(
        self,
        processed_query: str,
        query_embedding: List[float],
        vector_store: VectorStoreStrategy,
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        """Delegates query embedding vector search to the injected VectorStoreStrategy."""
        return await vector_store.search(
            query_embedding=query_embedding,
            limit=limit,
            metadata_filter=metadata_filter,
        )
