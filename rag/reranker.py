import os
from typing import List, Dict


# =========================================================
# CONFIGURATION
# =========================================================

ENABLE_RERANKER = (
    os.getenv(
        "ENABLE_RERANKER",
        "false"
    ).lower()
    == "true"
)

RERANKER_MODEL = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# =========================================================
# RERANKER
# =========================================================

class FarmingReranker:

    def __init__(self):

        self.model = None

        if not ENABLE_RERANKER:

            print(
                "Reranker disabled "
                "(memory-safe mode)."
            )

            return

        print(
            "Loading reranker..."
        )

        try:

            from sentence_transformers import (
                CrossEncoder
            )

            self.model = CrossEncoder(
                RERANKER_MODEL
            )

            print(
                f"Reranker loaded: "
                f"{RERANKER_MODEL}"
            )

        except Exception as e:

            print(
                "Reranker unavailable."
            )

            print(
                f"Reason: {e}"
            )

            self.model = None


    def rerank(
        self,
        query: str,
        candidates: List[Dict],
        top_k: int = 5
    ) -> List[Dict]:

        if not candidates:

            return []

        # -------------------------------------------------
        # DISABLED / FAILED
        # -------------------------------------------------

        if self.model is None:

            return candidates[:top_k]

        # -------------------------------------------------
        # CROSS ENCODER
        # -------------------------------------------------

        pairs = [

            [
                query,
                candidate.get(
                    "text",
                    ""
                )
            ]

            for candidate in candidates

        ]

        scores = self.model.predict(
            pairs
        )

        ranked = []

        for candidate, score in zip(
            candidates,
            scores
        ):

            result = candidate.copy()

            result[
                "rerank_score"
            ] = float(score)

            ranked.append(
                result
            )

        ranked.sort(
            key=lambda x:
                x.get(
                    "rerank_score",
                    0
                ),
            reverse=True
        )

        return ranked[:top_k]


# =========================================================
# RETRIEVE + RERANK
# =========================================================

def retrieve_and_rerank(
    query: str,
    candidate_k: int = 20,
    final_k: int = 5
):

    # -----------------------------------------------------
    # Lazy import
    # -----------------------------------------------------

    from rag.retriever import (
        HybridRetriever
    )

    retriever = HybridRetriever()

    # -----------------------------------------------------
    # RETRIEVE
    # -----------------------------------------------------

    candidates = retriever.hybrid_search(
        query,
        top_k=candidate_k
    )

    print(
        f"\nCandidates retrieved: "
        f"{len(candidates)}"
    )

    # -----------------------------------------------------
    # RERANK
    # -----------------------------------------------------

    reranker = FarmingReranker()

    results = reranker.rerank(
        query,
        candidates,
        top_k=final_k
    )

    print(
        f"After reranking: "
        f"{len(results)}"
    )

    return results


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    queries = [

        "My rice leaves are turning yellow. What should I do?",

        "paddy leaf yellowing",

        "rice disease precautions",

    ]

    for query in queries:

        print(
            "\n" + "=" * 70
        )

        print(
            "QUERY:"
        )

        print(
            query
        )

        print(
            "=" * 70
        )

        results = retrieve_and_rerank(
            query,
            candidate_k=20,
            final_k=5
        )

        for i, result in enumerate(
            results,
            start=1
        ):

            print(
                "\n" + "-" * 70
            )

            print(
                f"RESULT {i}"
            )

            print(
                f"Page: "
                f"{result.get('page')}"
            )

            print(
                f"Chunk: "
                f"{result.get('chunk_id')}"
            )

            print(
                f"Hybrid score: "
                f"{result.get('hybrid_score', 0):.4f}"
            )

            print(
                f"Rerank score: "
                f"{result.get('rerank_score', 0):.4f}"
            )

            print(
                "\nText:"
            )

            print(
                result.get(
                    "text",
                    ""
                )[:700]
            )