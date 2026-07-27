"""Factory for Vector Store Strategies."""

from app.interfaces.vectorstore_strategy import VectorStoreStrategy
from app.strategies.vectorstore.chroma_vectorstore_strategy import (
    ChromaVectorStoreStrategy,
)


class VectorStoreFactory:
    """Factory creating instances of VectorStoreStrategy based on configuration."""

    @staticmethod
    def create(
        provider_name: str = "chroma",
        persist_directory: str = "../travel-knowledge-ingestion/chroma",
        collection_name: str = "travel_knowledge",
    ) -> VectorStoreStrategy:
        """Instantiates specified vector store strategy."""
        normalized_name = provider_name.lower().strip()
        if normalized_name == "chroma":
            return ChromaVectorStoreStrategy(
                persist_directory=persist_directory,
                collection_name=collection_name,
            )
        else:
            raise ValueError(
                f"Unsupported vector store provider '{provider_name}'. "
                "Supported provider: 'chroma'."
            )
