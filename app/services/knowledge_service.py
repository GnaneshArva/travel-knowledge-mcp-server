"""Knowledge Service handling domain business logic."""

from typing import Optional
from app.dto.request import KnowledgeSearchRequest
from app.dto.response import KnowledgeSearchResponse
from app.pipeline.knowledge_pipeline import KnowledgeRetrievalPipeline
from app.utils.logger import get_logger

logger = get_logger(__name__)


class KnowledgeService:
    """Enterprise Business Service for Knowledge Retrieval.

    Encapsulates domain-level queries while delegating vector retrieval
    and pipeline orchestration strictly to KnowledgeRetrievalPipeline.
    """

    def __init__(self, pipeline: KnowledgeRetrievalPipeline):
        self.pipeline = pipeline

    async def search_knowledge(
        self, request: KnowledgeSearchRequest
    ) -> KnowledgeSearchResponse:
        """Executes generic knowledge retrieval search via pipeline."""
        return await self.pipeline.execute(request)

    async def search_country_information(
        self, query: str, country: Optional[str] = None, limit: int = 5
    ) -> KnowledgeSearchResponse:
        """Retrieves destination and country information."""
        logger.info(
            f"Domain Service: search_country_information query='{query}', country='{country}'"
        )
        effective_query = query
        if country and country.lower() not in query.lower():
            effective_query = f"{query} for {country}"

        request = KnowledgeSearchRequest(
            query=effective_query,
            country=country,
            category="destination",
            limit=limit,
        )
        return await self.pipeline.execute(request)

    async def search_visa_requirements(
        self, query: str, country: Optional[str] = None, limit: int = 5
    ) -> KnowledgeSearchResponse:
        """Retrieves visa, passport, and entry requirements."""
        logger.info(
            f"Domain Service: search_visa_requirements query='{query}', country='{country}'"
        )
        effective_query = query
        if country and country.lower() not in query.lower():
            effective_query = f"{query} for {country}"

        request = KnowledgeSearchRequest(
            query=effective_query,
            country=country,
            category="visa",
            limit=limit,
        )
        return await self.pipeline.execute(request)

    async def search_travel_guidelines(
        self, query: str, category: Optional[str] = None, limit: int = 5
    ) -> KnowledgeSearchResponse:
        """Retrieves travel guidelines, safety tips, and general advice."""
        logger.info(
            f"Domain Service: search_travel_guidelines query='{query}', category='{category}'"
        )
        request = KnowledgeSearchRequest(
            query=query,
            country=None,
            category=category or "guidelines",
            limit=limit,
        )
        return await self.pipeline.execute(request)
