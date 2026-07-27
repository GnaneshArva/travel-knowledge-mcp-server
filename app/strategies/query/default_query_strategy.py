"""Default Query Processing Strategy."""

from app.interfaces.query_strategy import QueryProcessingStrategy


class DefaultQueryProcessingStrategy(QueryProcessingStrategy):
    """Default strategy that performs basic query normalization."""

    async def process_query(self, query: str) -> str:
        """Trims leading/trailing whitespace and normalizes query string."""
        if not query:
            return ""
        return query.strip()
