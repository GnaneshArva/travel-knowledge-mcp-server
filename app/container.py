"""Dependency Injection Container and Composition Root."""

from app.config.settings import Settings, settings
from app.factories.embedding_factory import EmbeddingFactory
from app.factories.query_factory import QueryStrategyFactory
from app.factories.reranking_factory import RerankingStrategyFactory
from app.factories.retrieval_factory import RetrievalStrategyFactory
from app.factories.vectorstore_factory import VectorStoreFactory
from app.pipeline.knowledge_pipeline import KnowledgeRetrievalPipeline
from app.services.knowledge_service import KnowledgeService


def create_knowledge_service(
    settings_obj: Settings = settings,
) -> KnowledgeService:
    """Instantiates and wires all dependencies via factories based on configuration."""
    query_strategy = QueryStrategyFactory.create(settings_obj.QUERY_STRATEGY)

    vector_store_strategy = VectorStoreFactory.create(
        provider_name=settings_obj.VECTOR_STORE,
        persist_directory=settings_obj.CHROMA_PERSIST_DIRECTORY,
        collection_name=settings_obj.CHROMA_COLLECTION,
    )

    retrieval_strategy = RetrievalStrategyFactory.create(
        settings_obj.RETRIEVAL_STRATEGY
    )

    reranking_strategy = RerankingStrategyFactory.create(
        settings_obj.RERANKING_STRATEGY
    )

    embedding_provider = EmbeddingFactory.create(
        provider_name=settings_obj.EMBEDDING_PROVIDER,
        model_name=settings_obj.EMBEDDING_MODEL,
    )

    pipeline = KnowledgeRetrievalPipeline(
        query_strategy=query_strategy,
        embedding_provider=embedding_provider,
        retrieval_strategy=retrieval_strategy,
        vector_store_strategy=vector_store_strategy,
        reranking_strategy=reranking_strategy,
    )

    return KnowledgeService(pipeline=pipeline)
