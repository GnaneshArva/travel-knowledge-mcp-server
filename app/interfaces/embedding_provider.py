"""Embedding Provider interface definition."""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Abstract interface for text embedding generation."""

    @abstractmethod
    async def embed_query(self, text: str) -> list[float]:
        """Generates an embedding vector for a search query string."""
        pass
