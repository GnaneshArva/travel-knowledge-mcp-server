"""MCP Resources module exposing static/dynamic context."""

import json
from fastmcp import FastMCP
from app.utils.logger import get_logger

logger = get_logger(__name__)


def register_knowledge_resources(mcp: FastMCP) -> None:
    """Registers official MCP Resources on the FastMCP server instance."""

    @mcp.resource(
        "knowledge://categories",
        name="knowledge-categories",
        description="Returns list of available knowledge categories indexed in ChromaDB.",
    )
    def get_knowledge_categories() -> str:
        """Returns JSON serialized knowledge categories."""
        categories = {
            "categories": [
                "destination",
                "visa",
                "guidelines",
                "safety",
                "health",
                "culture",
                "transportation",
            ]
        }
        return json.dumps(categories, indent=2)

    @mcp.resource(
        "knowledge://countries",
        name="supported-countries",
        description="Returns list of supported countries with available travel knowledge.",
    )
    def get_supported_countries() -> str:
        """Returns JSON serialized supported country list."""
        countries = {
            "countries": [
                "Japan",
                "France",
                "Italy",
                "Thailand",
                "Australia",
                "Brazil",
                "Canada",
                "United Kingdom",
                "United States",
                "Germany",
            ]
        }
        return json.dumps(countries, indent=2)

    @mcp.resource(
        "knowledge://version",
        name="knowledge-version",
        description="Returns metadata about the travel knowledge base version.",
    )
    def get_knowledge_version() -> str:
        """Returns version and schema information for the knowledge base."""
        version_info = {
            "version": "2.0.0",
            "server": "travel-knowledge-mcp-server",
            "embedding_model": "all-MiniLM-L6-v2",
            "vector_store": "ChromaDB",
            "last_updated": "2026-07-27",
        }
        return json.dumps(version_info, indent=2)
