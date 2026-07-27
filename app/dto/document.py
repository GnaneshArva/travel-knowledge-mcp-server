"""Document and Citation DTO definitions."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class CitationDto(BaseModel):
    """DTO representing source citation for retrieved knowledge."""

    document_id: str = Field(..., description="Unique document chunk identifier")
    source: str = Field(..., description="File source or document reference")
    country: Optional[str] = Field(
        default=None, description="Associated country if applicable"
    )
    category: Optional[str] = Field(
        default=None, description="Knowledge category"
    )
    score: float = Field(
        default=0.0, description="Relevance score or similarity metric"
    )


class RetrievedDocumentDto(BaseModel):
    """DTO representing a single retrieved document chunk."""

    document_id: str = Field(..., description="Unique chunk ID")
    content: str = Field(..., description="Text content of the retrieved chunk")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Chunk metadata attributes"
    )
    score: float = Field(
        default=0.0, description="Similarity or relevance score"
    )
    source: str = Field(
        default="unknown", description="Source document path or name"
    )
