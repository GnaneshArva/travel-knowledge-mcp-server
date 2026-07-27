"""Factory for Query Processing Strategies."""

from app.interfaces.query_strategy import QueryProcessingStrategy
from app.strategies.query.default_query_strategy import (
    DefaultQueryProcessingStrategy,
)


class QueryStrategyFactory:
    """Factory creating instances of QueryProcessingStrategy based on configuration."""

    @staticmethod
    def create(strategy_name: str = "default") -> QueryProcessingStrategy:
        """Instantiates specified query processing strategy."""
        normalized_name = strategy_name.lower().strip()
        if normalized_name == "default":
            return DefaultQueryProcessingStrategy()
        else:
            raise ValueError(
                f"Unsupported query strategy '{strategy_name}'. "
                "Supported strategy: 'default'."
            )
