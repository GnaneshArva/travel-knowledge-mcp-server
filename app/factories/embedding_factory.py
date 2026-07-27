"""Factory for Embedding Providers."""

from app.implementations.embedding.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)
from app.interfaces.embedding_provider import EmbeddingProvider


class EmbeddingFactory:
    """Factory creating instances of EmbeddingProvider based on configuration."""

    @staticmethod
    def create(
        provider_name: str = "sentence-transformers",
        model_name: str = "all-MiniLM-L6-v2",
    ) -> EmbeddingProvider:
        """Instantiates specified embedding provider."""
        normalized_name = provider_name.lower().strip()
        if normalized_name in [
            "sentence-transformers",
            "sentence_transformers",
            "sentencetransformers",
        ]:
            return SentenceTransformerEmbeddingProvider(model_name=model_name)
        else:
            raise ValueError(
                f"Unsupported embedding provider '{provider_name}'. "
                "Supported provider: 'sentence-transformers'."
            )
