"""MCP Prompt Templates module providing structured context prompts."""

from fastmcp import FastMCP
from app.utils.logger import get_logger

logger = get_logger(__name__)


def register_knowledge_prompts(mcp: FastMCP) -> None:
    """Registers official MCP Prompt Templates on the FastMCP server instance."""

    @mcp.prompt(
        name="destination-guide",
        description="Generates a structured prompt template for building a comprehensive destination guide.",
    )
    def destination_guide(
        destination: str,
        duration: str = "7 days",
        interests: str = "culture, food, history",
    ) -> str:
        """Prompt template for destination itinerary and guide."""
        return f"""You are an expert travel assistant. Please use the `search_country_information` MCP tool to retrieve official knowledge about {destination}.

Parameters provided:
- Destination: {destination}
- Duration: {duration}
- Interests: {interests}

Instructions:
1. Search for relevant attractions, local customs, and neighborhood guides for {destination}.
2. Synthesize the retrieved knowledge chunks into a structured day-by-day itinerary tailored to interests in {interests}.
3. Include specific citations to the retrieved knowledge sources.
"""

    @mcp.prompt(
        name="visa-summary",
        description="Generates a structured prompt template for summarizing visa and entry requirements.",
    )
    def visa_summary(
        origin_country: str,
        destination_country: str,
        passport_type: str = "regular",
    ) -> str:
        """Prompt template for visa and passport requirement analysis."""
        return f"""You are an international immigration and travel compliance specialist.

Please use the `search_visa_requirements` MCP tool to retrieve official entry rules for travelers from {origin_country} visiting {destination_country}.

Details:
- Traveler Origin: {origin_country}
- Destination: {destination_country}
- Passport Type: {passport_type}

Instructions:
1. Query the knowledge base for visa exemptions, stay limits, passport validity requirements, and mandatory registration protocols.
2. Highlight critical deadlines, mandatory fees, and potential travel advisories.
3. List explicit source citations for all entry conditions.
"""

    @mcp.prompt(
        name="travel-advisor",
        description="Generates a structured prompt template for general travel advisory and safety planning.",
    )
    def travel_advisor(
        query: str,
        target_audience: str = "solo traveler",
    ) -> str:
        """Prompt template for travel guidelines and advisory requests."""
        return f"""You are a professional travel safety advisor.

Please use the `search_travel_guidelines` MCP tool to answer the user query: "{query}" for a {target_audience}.

Instructions:
1. Retrieve up-to-date travel guidelines, health recommendations, and safety precautions matching the query.
2. Provide clear, actionable advice organized by priority.
3. Cite the relevant retrieved knowledge items.
"""
