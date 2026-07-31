"""Query Rewriting Strategy."""

import re
from app.interfaces.query_strategy import QueryProcessingStrategy


class QueryRewritingStrategy(QueryProcessingStrategy):
    """Normalizes, expands synonyms, and cleans input queries for higher vector search precision."""

    def __init__(self):
        self.synonyms = {
            "flight": ["airline", "flight ticket", "air travel"],
            "hotel": ["accommodation", "stay", "resort", "lodging"],
            "visa": ["entry requirement", "passport rules", "immigration"],
            "weather": ["climate", "temperature", "forecast"],
        }

    async def process_query(self, query: str) -> str:
        cleaned = re.sub(r"[^\w\s]", " ", query.lower()).strip()
        expanded_terms = [cleaned]

        for term, expansion in self.synonyms.items():
            if term in cleaned:
                expanded_terms.extend(expansion[:2])

        return " ".join(expanded_terms)
