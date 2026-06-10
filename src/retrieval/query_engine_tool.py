"""Placeholder for Member 1's legal retrieval tool.

Member 1 will replace this file with the real legal retrieval implementation.
Member 2 should depend on the public query interface only, not on retrieval
internals such as chunking, vector stores, or reranking.
"""


class QueryEngineTool:
    """Placeholder interface for the future legal retrieval tool."""

    def query(self, question: str, top_k: int = 3) -> list[dict]:
        """Return top-k legal results for a user question.

        The real implementation should return dictionaries with fields such as:
        document_name, article, effective_status, excerpt, source, metadata, and
        retrieval_score.
        """

        raise NotImplementedError(
            "Member 1 must implement QueryEngineTool.query before production use."
        )
