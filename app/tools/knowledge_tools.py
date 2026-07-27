"""MCP Tools module exposing Knowledge Retrieval capabilities."""

from typing import Optional
from fastmcp import FastMCP
from app.dto.response import KnowledgeSearchResponse
from app.services.knowledge_service import KnowledgeService
from app.utils.logger import get_logger

logger = get_logger(__name__)


def register_knowledge_tools(mcp: FastMCP, service: KnowledgeService) -> None:
    """Registers official MCP Tools on the FastMCP server instance."""

    @mcp.tool(
        name="search_country_information",
        description="Retrieve destination and country travel information, attractions, and cultural background.",
    )
    async def search_country_information(
        query: str,
        country: Optional[str] = None,
        limit: int = 5,
    ) -> KnowledgeSearchResponse:
        """Retrieve destination information."""
        logger.info(
            f"MCP Tool 'search_country_information' called: query='{query}', country='{country}'"
        )
        return await service.search_country_information(
            query=query, country=country, limit=limit
        )

    @mcp.tool(
        name="search_visa_requirements",
        description="Retrieve visa, passport, entry rules, and official diplomatic requirements for travelers.",
    )
    async def search_visa_requirements(
        query: str,
        country: Optional[str] = None,
        limit: int = 5,
    ) -> KnowledgeSearchResponse:
        """Retrieve visa requirements."""
        logger.info(
            f"MCP Tool 'search_visa_requirements' called: query='{query}', country='{country}'"
        )
        return await service.search_visa_requirements(
            query=query, country=country, limit=limit
        )

    @mcp.tool(
        name="search_travel_guidelines",
        description="Retrieve general travel guidelines, safety advisories, health regulations, and packing tips.",
    )
    async def search_travel_guidelines(
        query: str,
        category: Optional[str] = None,
        limit: int = 5,
    ) -> KnowledgeSearchResponse:
        """Retrieve travel guidelines."""
        logger.info(
            f"MCP Tool 'search_travel_guidelines' called: query='{query}', category='{category}'"
        )
        return await service.search_travel_guidelines(
            query=query, category=category, limit=limit
        )
