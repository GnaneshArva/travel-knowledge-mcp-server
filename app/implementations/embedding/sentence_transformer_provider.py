"""SentenceTransformer embedding provider implementation."""

import asyncio
from typing import List
from sentence_transformers import SentenceTransformer
from app.interfaces.embedding_provider import EmbeddingProvider
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    """Generates text embeddings using local SentenceTransformer models."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            logger.info(
                f"Initializing SentenceTransformer model: '{self.model_name}'"
            )
            self._model = SentenceTransformer(self.model_name)
        return self._model

    async def embed_query(self, text: str) -> List[float]:
        """Embeds text query asynchronously into a vector representation."""
        loop = asyncio.get_running_loop()
        model = self._get_model()

        def _encode() -> List[float]:
            vector = model.encode(text, convert_to_numpy=True)
            return vector.tolist()

        return await loop.run_in_executor(None, _encode)
