import math
from typing import List, Dict, Any


class MMRReranker:
    """Maximal Marginal Relevance (MMR) re-ranker balancing query relevance and result diversity."""

    def __init__(self, lambda_param: float = 0.5):
        self.lambda_param = lambda_param

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        if not documents:
            return []

        selected: List[Dict[str, Any]] = []
        unselected = list(documents)

        while len(selected) < top_k and unselected:
            best_doc = None
            best_mmr = -float("inf")

            for doc in unselected:
                rel = float(doc.get("score", 0.8))
                # Diversity penalty relative to already selected docs
                sim_to_selected = 0.0
                if selected:
                    sim_to_selected = max([
                        self._jaccard_sim(doc.get("content", ""), sel.get("content", ""))
                        for sel in selected
                    ])

                mmr_score = (self.lambda_param * rel) - ((1 - self.lambda_param) * sim_to_selected)
                if mmr_score > best_mmr:
                    best_mmr = mmr_score
                    best_doc = doc

            if best_doc:
                doc_copy = dict(best_doc)
                doc_copy["mmr_score"] = round(best_mmr, 4)
                selected.append(doc_copy)
                unselected.remove(best_doc)

        return selected

    def _jaccard_sim(self, text1: str, text2: str) -> float:
        w1, w2 = set(text1.lower().split()), set(text2.lower().split())
        if not w1 or not w2:
            return 0.0
        return len(w1 & w2) / len(w1 | w2)
