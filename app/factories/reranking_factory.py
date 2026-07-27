"""Factory for Reranking Strategies."""

from app.interfaces.reranking_strategy import RerankingStrategy
from app.strategies.reranking.no_op_reranking_strategy import (
    NoOpRerankingStrategy,
)


class RerankingStrategyFactory:
    """Factory creating instances of RerankingStrategy based on configuration."""

    @staticmethod
    def create(strategy_name: str = "no_op") -> RerankingStrategy:
        """Instantiates specified reranking strategy."""
        normalized_name = strategy_name.lower().strip()
        if normalized_name in ["no_op", "none", "noop"]:
            return NoOpRerankingStrategy()
        else:
            raise ValueError(
                f"Unsupported reranking strategy '{strategy_name}'. "
                "Supported strategy: 'no_op'."
            )
