"""HyDE (Hypothetical Document Embeddings) Strategy."""

from app.interfaces.query_strategy import QueryProcessingStrategy


class HyDEQueryStrategy(QueryProcessingStrategy):
    """Generates a hypothetical answer document for embedding similarity matching."""

    async def process_query(self, query: str) -> str:
        # Generates synthetic hypothetical answer document text
        hypothetical_doc = (
            f"The following travel guide provides details for {query}. "
            f"Key attractions, transportation options, entry requirements, and hotel recommendations for {query}."
        )
        return hypothetical_doc
