"""Response and Result DTO definitions."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.dto.document import CitationDto, RetrievedDocumentDto


class KnowledgeResultDto(BaseModel):
    """Domain-level structured result containing knowledge details."""

    title: str = Field(..., description="Result title or document summary tag")
    summary: str = Field(..., description="Key excerpt or summary content")
    category: Optional[str] = Field(default=None, description="Domain category")
    country: Optional[str] = Field(default=None, description="Target country")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class KnowledgeSearchResponse(BaseModel):
    """DTO representing the complete result of a knowledge retrieval search."""

    query: str = Field(..., description="Original user search query")
    processed_query: str = Field(
        ..., description="Query after pipeline processing strategy"
    )
    total_results: int = Field(..., description="Number of retrieved documents")
    documents: List[RetrievedDocumentDto] = Field(
        default_factory=list, description="Retrieved document list"
    )
    citations: List[CitationDto] = Field(
        default_factory=list, description="Citations for retrieved knowledge"
    )
    execution_time_ms: float = Field(
        default=0.0, description="Retrieval pipeline execution latency in ms"
    )
