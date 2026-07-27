"""Application Configuration Module."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for travel-knowledge-mcp-server."""

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Enterprise RAG Strategy Selection
    VECTOR_STORE: str = "chroma"
    RETRIEVAL_STRATEGY: str = "vector_similarity"
    QUERY_STRATEGY: str = "default"
    RERANKING_STRATEGY: str = "no_op"
    EMBEDDING_PROVIDER: str = "sentence-transformers"

    # Model Parameters
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    TOP_K: int = 5

    # Vector Store Connection Details
    CHROMA_COLLECTION: str = "travel_knowledge"
    CHROMA_PERSIST_DIRECTORY: str = "../travel-knowledge-ingestion/chroma"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Singleton settings instance
settings = Settings()
