"""Request DTO definitions for Knowledge Retrieval."""

from typing import Optional
from pydantic import BaseModel, Field


class KnowledgeSearchRequest(BaseModel):
    """DTO representing a knowledge search request."""

    query: str = Field(..., description="The search query text")
    country: Optional[str] = Field(
        default=None, description="Optional target country filter"
    )
    category: Optional[str] = Field(
        default=None, description="Optional target category filter"
    )
    limit: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Maximum number of results to retrieve",
    )
