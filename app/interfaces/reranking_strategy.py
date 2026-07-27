"""Reranking Strategy interface definition."""

from abc import ABC, abstractmethod
from typing import List
from app.dto.document import RetrievedDocumentDto


class RerankingStrategy(ABC):
    """Abstract strategy interface for post-retrieval document reranking."""

    @abstractmethod
    async def rerank(
        self, query: str, documents: List[RetrievedDocumentDto]
    ) -> List[RetrievedDocumentDto]:
        """Reranks retrieved document candidates against the query."""
        pass
