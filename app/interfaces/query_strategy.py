"""Query Processing Strategy interface definition."""

from abc import ABC, abstractmethod


class QueryProcessingStrategy(ABC):
    """Abstract strategy interface for pre-processing user queries before retrieval."""

    @abstractmethod
    async def process_query(self, query: str) -> str:
        """Transforms or expands the input query string."""
        pass
