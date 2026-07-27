"""Vector Store Strategy interface definition."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.dto.document import RetrievedDocumentDto


class VectorStoreStrategy(ABC):
    """Abstract interface for low-level vector store operations."""

    @abstractmethod
    async def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        """Searches vector store using query embedding and optional metadata filters."""
        pass
