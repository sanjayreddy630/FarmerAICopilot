import re

from typing import List, Dict


# =========================================================
# NOISE PATTERNS
# =========================================================

NOISE_PATTERNS = [

    "recommended fields:",

    "farmer / rag questions",

    "example data record",

]


# =========================================================
# WORD EXTRACTION
# =========================================================

def words(text: str):

    return set(

        re.findall(

            r"\b[a-zA-Z]{3,}\b",

            text.lower()

        )

    )


# =========================================================
# AGRICULTURAL IMPORTANT TERMS
# =========================================================

IMPORTANT_TERMS = {

    "rice",
    "paddy",
    "yellow",
    "yellowing",
    "leaf",
    "leaves",
    "disease",
    "infection",
    "symptom",
    "pest",
    "management",
    "precaution",
    "control",
    "treatment",
    "irrigation",
    "water",
    "nutrient",
    "nutrition",
    "fertilizer",
    "nitrogen",
    "deficiency",
    "rain",
    "rainy",
    "season",
    "kharif",
    "rabi",
    "crop",

}


# =========================================================
# KEYWORD OVERLAP
# =========================================================

def keyword_overlap(
    query: str,
    text: str
) -> float:

    query_words = words(
        query
    )

    text_words = words(
        text
    )


    if not query_words:

        return 0.0


    overlap = (
        query_words &
        text_words
    )


    return (
        len(overlap) /
        len(query_words)
    )


# =========================================================
# IMPORTANT TERM OVERLAP
# =========================================================

def important_term_overlap(
    query: str,
    text: str
) -> float:

    query_words = words(
        query
    )

    text_words = words(
        text
    )


    important_query_words = (

        query_words &
        IMPORTANT_TERMS

    )


    if not important_query_words:

        return 0.0


    overlap = (

        important_query_words &
        text_words

    )


    return (

        len(overlap) /
        len(important_query_words)

    )


# =========================================================
# NOISE SCORE
# =========================================================

def noise_score(
    text: str
) -> float:

    lower = text.lower()

    score = 0.0


    for pattern in NOISE_PATTERNS:

        if pattern in lower:

            score += 1.0


    return score


# =========================================================
# FINAL SCORE
# =========================================================

def final_score(
    query: str,
    result: Dict
) -> float:

    rerank = float(

        result.get(
            "rerank_score",
            0.0
        )

    )


    hybrid = float(

        result.get(
            "hybrid_score",
            0.0
        )

    )


    overlap = keyword_overlap(

        query,

        result.get(
            "text",
            ""
        )

    )


    important_overlap = (
        important_term_overlap(

            query,

            result.get(
                "text",
                ""
            )

        )
    )


    noise = noise_score(

        result.get(
            "text",
            ""
        )

    )


    # ---------------------------------------------
    # SCORING
    # ---------------------------------------------

    score = (

        rerank

        + hybrid * 1.5

        + overlap * 2.0

        + important_overlap * 2.5

        - noise * 0.25

    )


    return score


# =========================================================
# FILTER RESULTS
# =========================================================

def filter_results(

    query: str,

    results: List[Dict],

    top_k: int = 5

) -> List[Dict]:

    scored = []


    for result in results:

        result = result.copy()


        result[
            "keyword_overlap"
        ] = keyword_overlap(

            query,

            result.get(
                "text",
                ""
            )

        )


        result[
            "important_overlap"
        ] = important_term_overlap(

            query,

            result.get(
                "text",
                ""
            )

        )


        result[
            "noise_score"
        ] = noise_score(

            result.get(
                "text",
                ""
            )

        )


        result[
            "final_score"
        ] = final_score(

            query,

            result

        )


        scored.append(
            result
        )


    # ---------------------------------------------
    # SORT
    # ---------------------------------------------

    scored.sort(

        key=lambda x:
            x.get(
                "final_score",
                0
            ),

        reverse=True

    )


    # ---------------------------------------------
    # RETURN TOP RESULTS
    # ---------------------------------------------

    return scored[:top_k]


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    from rag.reranker import (
        retrieve_and_rerank
    )


    query = (
        "My rice leaves are turning "
        "yellow. What should I do?"
    )


    print("=" * 70)

    print(
        "RELEVANCE FILTER TEST"
    )

    print("=" * 70)


    results = retrieve_and_rerank(

        query,

        candidate_k=20,

        final_k=10

    )


    filtered = filter_results(

        query,

        results,

        top_k=5

    )


    print(
        f"\nCandidates: "
        f"{len(results)}"
    )


    print(
        f"Final results: "
        f"{len(filtered)}"
    )


    for i, result in enumerate(

        filtered,

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
            f"Hybrid score: "
            f"{result.get('hybrid_score', 0):.4f}"
        )


        print(
            f"Rerank score: "
            f"{result.get('rerank_score', 0):.4f}"
        )


        print(
            f"Keyword overlap: "
            f"{result.get('keyword_overlap', 0):.4f}"
        )


        print(
            f"Important overlap: "
            f"{result.get('important_overlap', 0):.4f}"
        )


        print(
            f"Noise score: "
            f"{result.get('noise_score', 0):.4f}"
        )


        print(
            f"Final score: "
            f"{result.get('final_score', 0):.4f}"
        )


        print("\nText:")


        print(
            result.get(
                "text",
                ""
            )[:900]
        )