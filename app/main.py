"""Main Application Entry Point for travel-knowledge-mcp-server."""

import os
import sys
from pathlib import Path
from fastmcp import FastMCP

# Ensure app package is in Python module search path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from app.config.settings import settings
from app.container import create_knowledge_service
from app.prompts.knowledge_prompts import register_knowledge_prompts
from app.resources.knowledge_resources import register_knowledge_resources
from app.tools.knowledge_tools import register_knowledge_tools
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize FastMCP Server
mcp = FastMCP(
    name="travel-knowledge-mcp-server",
    instructions="Enterprise Knowledge Retrieval (RAG) MCP Server for Travel Planner",
)

# Initialize Dependency Injection Container & Service
knowledge_service = create_knowledge_service(settings)

# Register MCP Components
register_knowledge_tools(mcp, knowledge_service)
register_knowledge_resources(mcp)
register_knowledge_prompts(mcp)


def main():
    """Starts the FastMCP server."""
    logger.info(
        f"Starting travel-knowledge-mcp-server with strategy: "
        f"[VectorStore: {settings.VECTOR_STORE}, Retrieval: {settings.RETRIEVAL_STRATEGY}, Query: {settings.QUERY_STRATEGY}, Reranking: {settings.RERANKING_STRATEGY}]"
    )
    # FastMCP run handles stdio/SSE protocol depending on command flags or default stdio
    mcp.run()


if __name__ == "__main__":
    main()
