"""Retrieval Strategy interface definition."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.dto.document import RetrievedDocumentDto
from app.interfaces.vectorstore_strategy import VectorStoreStrategy


class RetrievalStrategy(ABC):
    """Abstract strategy interface for document retrieval logic.

    Note: Implementations must decouple high-level retrieval algorithm
    from specific vector database APIs by relying on VectorStoreStrategy.
    """

    @abstractmethod
    async def retrieve(
        self,
        processed_query: str,
        query_embedding: List[float],
        vector_store: VectorStoreStrategy,
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        """Retrieves documents using vector store strategy."""
        pass
