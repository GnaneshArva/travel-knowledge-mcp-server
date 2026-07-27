"""ChromaDB Vector Store Strategy implementation."""

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
import chromadb
from app.dto.document import RetrievedDocumentDto
from app.interfaces.vectorstore_strategy import VectorStoreStrategy
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ChromaVectorStoreStrategy(VectorStoreStrategy):
    """VectorStoreStrategy implementation connecting to persistent ChromaDB."""

    def __init__(
        self,
        persist_directory: str = "../travel-knowledge-ingestion/chroma",
        collection_name: str = "travel_knowledge",
    ):
        self.persist_directory = str(Path(persist_directory).resolve())
        self.collection_name = collection_name
        self._client: Optional[chromadb.PersistentClient] = None
        self._collection = None

    def _get_collection(self):
        if self._collection is None:
            logger.info(
                f"Connecting to ChromaDB at: '{self.persist_directory}' "
                f"for collection: '{self.collection_name}'"
            )
            self._client = chromadb.PersistentClient(path=self.persist_directory)
            try:
                self._collection = self._client.get_collection(
                    name=self.collection_name
                )
            except Exception as exc:
                logger.error(
                    f"Failed to load collection '{self.collection_name}' from ChromaDB: {exc}"
                )
                raise RuntimeError(
                    f"ChromaDB collection '{self.collection_name}' not found at '{self.persist_directory}'. "
                    "Ensure travel-knowledge-ingestion has run first."
                ) from exc
        return self._collection

    def _build_where_clause(
        self, metadata_filter: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        if not metadata_filter:
            return None

        clean_filters = {
            k: v for k, v in metadata_filter.items() if v is not None
        }
        if not clean_filters:
            return None

        if len(clean_filters) == 1:
            k, v = next(iter(clean_filters.items()))
            return {k: v}

        return {"$and": [{k: v} for k, v in clean_filters.items()]}

    async def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocumentDto]:
        """Queries persistent ChromaDB collection with query embedding and metadata filters."""
        loop = asyncio.get_running_loop()
        collection = self._get_collection()
        where_clause = self._build_where_clause(metadata_filter)

        def _execute_query(where: Optional[Dict[str, Any]]):
            query_kwargs: Dict[str, Any] = {
                "query_embeddings": [query_embedding],
                "n_results": limit,
            }
            if where:
                query_kwargs["where"] = where

            return collection.query(**query_kwargs)

        # First try searching with metadata filter if provided
        results = await loop.run_in_executor(
            None, lambda: _execute_query(where_clause)
        )

        # Fallback to un-filtered vector search if strict metadata filter yields 0 matches
        if (
            where_clause
            and (not results or not results.get("ids") or not results["ids"][0])
        ):
            logger.warning(
                f"Metadata filter '{where_clause}' returned 0 results. "
                "Falling back to pure vector similarity search."
            )
            results = await loop.run_in_executor(
                None, lambda: _execute_query(None)
            )

        documents_dto: List[RetrievedDocumentDto] = []
        if not results or not results.get("ids") or not results["ids"][0]:
            return documents_dto

        ids = results["ids"][0]
        contents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = (
            results.get("distances", [[]])[0] if results.get("distances") else []
        )

        for idx in range(len(ids)):
            doc_id = ids[idx]
            content = contents[idx] if idx < len(contents) else ""
            meta = metadatas[idx] if idx < len(metadatas) and metadatas[idx] else {}
            dist = distances[idx] if idx < len(distances) else 0.0

            score = (
                round(max(0.0, 1.0 - float(dist)), 4) if dist is not None else 1.0
            )
            source = meta.get(
                "source",
                meta.get("document_name", meta.get("file_name", "ChromaDB")),
            )

            documents_dto.append(
                RetrievedDocumentDto(
                    document_id=str(doc_id),
                    content=content,
                    metadata=meta,
                    score=score,
                    source=str(source),
                )
            )

        return documents_dto
