"""Parent-Child Retrieval Strategy."""

from typing import Any, Dict, List, Optional
from app.dto.document import RetrievedDocumentDto
from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.interfaces.vectorstore_strategy import VectorStoreStrategy


class ParentChildRetrievalStrategy(RetrievalStrategy):
    """Searches granular child chunks for similarity, but resolves parent document context for final generation."""

    async def retrieve(
        self,
        processed_query: str,
        query_embedding: List[float],
        vector_store: VectorStoreStrategy,
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        # Search child vector chunks
        child_docs = await vector_store.search(
            query_embedding=query_embedding,
            limit=limit,
            metadata_filter=metadata_filter,
        )

        # Resolve parent context from metadata if available
        resolved_docs = []
        for doc in child_docs:
            parent_text = doc.metadata.get("parent_content") if doc.metadata else None
            if parent_text:
                resolved_docs.append(
                    RetrievedDocumentDto(
                        id=doc.id,
                        content=parent_text,
                        similarity_score=doc.similarity_score,
                        metadata=doc.metadata,
                    )
                )
            else:
                resolved_docs.append(doc)

        return resolved_docs
