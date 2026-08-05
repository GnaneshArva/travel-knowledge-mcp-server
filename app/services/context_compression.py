from typing import List, Dict, Any


class KnowledgeContextCompressor:
    """Token context compression engine for knowledge RAG passages."""

    def compress(self, passages: List[Dict[str, Any]], max_tokens: int = 500) -> List[Dict[str, Any]]:
        compressed = []
        token_count = 0

        for passage in passages:
            text = passage.get("content", "")
            words = text.split()
            estimated_tokens = len(words) * 1.3

            if token_count + estimated_tokens > max_tokens:
                break

            compressed.append(passage)
            token_count += estimated_tokens

        return compressed
