"""No-Op Reranking Strategy implementation."""

from typing import List
from app.dto.document import RetrievedDocumentDto
from app.interfaces.reranking_strategy import RerankingStrategy


class NoOpRerankingStrategy(RerankingStrategy):
    """Pass-through reranking strategy returning documents without modifying order."""

    async def rerank(
        self, query: str, documents: List[RetrievedDocumentDto]
    ) -> List[RetrievedDocumentDto]:
        """Returns retrieved document candidate list unmodified."""
        return documents
