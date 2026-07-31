"""Strategy Factory for instantiating all RAG retrieval and query strategies."""

from app.interfaces.query_strategy import QueryProcessingStrategy
from app.interfaces.retrieval_strategy import RetrievalStrategy
from app.strategies.query.default_query_strategy import DefaultQueryProcessingStrategy
from app.strategies.query.query_rewriting_strategy import QueryRewritingStrategy
from app.strategies.query.hyde_query_strategy import HyDEQueryStrategy

from app.strategies.retrieval.vector_similarity_strategy import VectorSimilarityRetrievalStrategy
from app.strategies.retrieval.hybrid_strategy import HybridRetrievalStrategy
from app.strategies.retrieval.metadata_filtering_strategy import MetadataFilteringRetrievalStrategy
from app.strategies.retrieval.multi_query_strategy import MultiQueryRetrievalStrategy
from app.strategies.retrieval.parent_child_strategy import ParentChildRetrievalStrategy
from app.strategies.retrieval.contextual_compression_strategy import ContextualCompressionRetrievalStrategy
from app.strategies.retrieval.agentic_strategy import AgenticRetrievalStrategy


class RetrievalStrategyFactory:
    """Factory instantiating active RetrievalStrategy based on configuration."""

    @staticmethod
    def create(strategy_name: str = "vector_similarity") -> RetrievalStrategy:
        name = strategy_name.lower().strip()
        if name in ["vector_similarity", "semantic", "vector"]:
            return VectorSimilarityRetrievalStrategy()
        elif name in ["hybrid", "bm25_hybrid"]:
            return HybridRetrievalStrategy()
        elif name in ["metadata", "metadata_filtering"]:
            return MetadataFilteringRetrievalStrategy()
        elif name in ["multi_query", "multiquery"]:
            return MultiQueryRetrievalStrategy()
        elif name in ["parent_child", "parentchild"]:
            return ParentChildRetrievalStrategy()
        elif name in ["compression", "contextual_compression"]:
            return ContextualCompressionRetrievalStrategy()
        elif name in ["agentic", "adaptive"]:
            return AgenticRetrievalStrategy()
        else:
            return VectorSimilarityRetrievalStrategy()


class QueryStrategyFactory:
    """Factory instantiating active QueryProcessingStrategy based on configuration."""

    @staticmethod
    def create(strategy_name: str = "default") -> QueryProcessingStrategy:
        name = strategy_name.lower().strip()
        if name in ["rewriting", "query_rewriting"]:
            return QueryRewritingStrategy()
        elif name in ["hyde", "hypothetical"]:
            return HyDEQueryStrategy()
        else:
            return DefaultQueryProcessingStrategy()
