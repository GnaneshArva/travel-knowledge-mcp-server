"""Enterprise Knowledge Retrieval Pipeline."""

import time
from typing import Any, Dict, List, Optional
from app.dto.document import CitationDto, RetrievedDocumentDto
from app.dto.request import KnowledgeSearchRequest
from app.dto.response import KnowledgeSearchResponse
from app.interfaces.embedding_provider import EmbeddingProvider
from app.interfaces.query_strategy import QueryProcessingStrategy
from app.interfaces.reranking_strategy import RerankingStrategy
from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.interfaces.vectorstore_strategy import VectorStoreStrategy
from app.utils.logger import get_logger

logger = get_logger(__name__)


class KnowledgeRetrievalPipeline:
    """Orchestrates the modular multi-stage Knowledge Retrieval Pipeline.

    Stages:
    1. Process Query (QueryProcessingStrategy)
    2. Embed Query (EmbeddingProvider)
    3. Retrieve Documents (RetrievalStrategy & VectorStoreStrategy)
    4. Rerank Candidates (RerankingStrategy)
    5. Construct DTO & Citations (KnowledgeSearchResponse)
    """

    def __init__(
        self,
        query_strategy: QueryProcessingStrategy,
        embedding_provider: EmbeddingProvider,
        retrieval_strategy: RetrievalStrategy,
        vector_store_strategy: VectorStoreStrategy,
        reranking_strategy: RerankingStrategy,
    ):
        self.query_strategy = query_strategy
        self.embedding_provider = embedding_provider
        self.retrieval_strategy = retrieval_strategy
        self.vector_store_strategy = vector_store_strategy
        self.reranking_strategy = reranking_strategy

    async def execute(
        self, request: KnowledgeSearchRequest
    ) -> KnowledgeSearchResponse:
        """Executes the complete retrieval pipeline end-to-end."""
        start_time = time.perf_counter()
        logger.info(
            f"Executing pipeline for query: '{request.query}' "
            f"[Country filter: {request.country}, Category filter: {request.category}, Limit: {request.limit}]"
        )

        # Stage 1: Query Pre-Processing
        processed_query = await self.query_strategy.process_query(request.query)

        # Stage 2: Query Embedding Generation
        query_embedding = await self.embedding_provider.embed_query(
            processed_query
        )

        # Build Metadata Filter Dict
        metadata_filter: Dict[str, Any] = {}
        if request.country:
            metadata_filter["country"] = request.country.strip().title()
        if request.category:
            metadata_filter["category"] = request.category.strip().lower()

        # Stage 3: Retrieval Execution
        retrieved_docs: List[
            RetrievedDocumentDto
        ] = await self.retrieval_strategy.retrieve(
            processed_query=processed_query,
            query_embedding=query_embedding,
            vector_store=self.vector_store_strategy,
            limit=request.limit,
            metadata_filter=metadata_filter if metadata_filter else None,
        )

        # Stage 4: Reranking Candidates
        reranked_docs: List[
            RetrievedDocumentDto
        ] = await self.reranking_strategy.rerank(
            query=processed_query, documents=retrieved_docs
        )

        # Stage 5: Citation Generation & Response Construction
        citations: List[CitationDto] = []
        for doc in reranked_docs:
            citations.append(
                CitationDto(
                    document_id=doc.document_id,
                    source=doc.source,
                    country=doc.metadata.get("country"),
                    category=doc.metadata.get("category"),
                    score=doc.score,
                )
            )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        logger.info(
            f"Pipeline execution completed in {elapsed_ms:.2f}ms. "
            f"Retrieved {len(reranked_docs)} candidate documents."
        )

        return KnowledgeSearchResponse(
            query=request.query,
            processed_query=processed_query,
            total_results=len(reranked_docs),
            documents=reranked_docs,
            citations=citations,
            execution_time_ms=round(elapsed_ms, 2),
        )
