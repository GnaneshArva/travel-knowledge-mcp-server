"""Factory for Retrieval Strategies."""

from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.strategies.retrieval.vector_similarity_strategy import (
    VectorSimilarityRetrievalStrategy,
)


class RetrievalStrategyFactory:
    """Factory creating instances of RetrievalStrategy based on configuration."""

    @staticmethod
    def create(strategy_name: str = "vector_similarity") -> RetrievalStrategy:
        """Instantiates specified document retrieval strategy."""
        normalized_name = strategy_name.lower().strip()
        if normalized_name in ["vector_similarity", "vector", "similarity"]:
            return VectorSimilarityRetrievalStrategy()
        else:
            raise ValueError(
                f"Unsupported retrieval strategy '{strategy_name}'. "
                "Supported strategy: 'vector_similarity'."
            )
