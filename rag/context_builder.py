from typing import List, Dict


def build_context(
    results: List[Dict],
    max_results: int = 5
) -> str:
    """
    Convert retrieved chunks into grounded LLM context
    with citation information.
    """

    context_parts = []

    for i, result in enumerate(
        results[:max_results],
        start=1
    ):

        page = result.get("page", "Unknown")
        chunk_id = result.get(
            "chunk_id",
            "Unknown"
        )

        metadata = result.get(
            "metadata",
            {}
        )

        text = result.get(
            "text",
            ""
        ).strip()

        citation = (
            f"[SOURCE {i} | "
            f"Farming Dataset | "
            f"Page {page} | "
            f"{chunk_id}]"
        )

        metadata_text = (
            f"Crop: {metadata.get('crop', '')}\n"
            f"Season: {metadata.get('season', '')}\n"
            f"Growth stage: "
            f"{metadata.get('growth_stage', '')}\n"
            f"Problem: "
            f"{metadata.get('problem', '')}\n"
            f"Technology: "
            f"{metadata.get('technology', '')}"
        )

        context_parts.append(
            f"{citation}\n"
            f"{metadata_text}\n\n"
            f"{text}"
        )

    return "\n\n" + ("\n\n" + "=" * 70 + "\n\n").join(
        context_parts
    )


def build_citations(
    results: List[Dict]
) -> List[Dict]:

    citations = []

    for i, result in enumerate(
        results,
        start=1
    ):

        citations.append({
            "id": i,
            "source": "Farming Dataset",
            "page": result.get("page"),
            "chunk_id": result.get(
                "chunk_id"
            ),
            "score": result.get(
                "rerank_score"
            ),
        })

    return citations


if __name__ == "__main__":

    from rag.reranker import (
        retrieve_and_rerank
    )

    query = (
        "What precautions should a farmer "
        "take for disease during Kharif season?"
    )

    results = retrieve_and_rerank(
        query,
        candidate_k=20,
        final_k=5
    )

    context = build_context(
        results
    )

    citations = build_citations(
        results
    )

    print("=" * 70)
    print("GROUNDED CONTEXT")
    print("=" * 70)

    print(context)

    print("\n")
    print("=" * 70)
    print("CITATIONS")
    print("=" * 70)

    for citation in citations:
        print(
            f"[{citation['id']}] "
            f"{citation['source']} — "
            f"Page {citation['page']}"
        )