import re


def clean_query(query: str) -> str:
    """
    Clean informal farmer questions before retrieval.
    """

    query = query.strip()

    # Normalize spaces
    query = re.sub(
        r"\s+",
        " ",
        query
    )

    return query


def expand_farming_query(query: str) -> str:
    """
    Add useful farming concepts to short/informal questions.
    This improves retrieval without changing the farmer's intent.
    """

    query = clean_query(query)

    lower = query.lower()

    expansions = []

    # Crop-related expansion
    crop_terms = {
        "paddy": "rice crop",
        "धान": "rice crop",
        "maize": "corn crop",
        "corn": "maize crop",
        "cotton": "cotton crop",
        "chilli": "chilli crop",
        "tomato": "tomato crop",
    }

    for word, expansion in crop_terms.items():

        if word in lower:
            expansions.append(expansion)

    # Symptom expansion
    symptom_terms = {
        "yellow": "yellowing leaves symptom",
        "yellowing": "yellow leaves symptom",
        "spots": "leaf spots disease symptom",
        "spot": "leaf spot disease symptom",
        "curl": "leaf curl symptom",
        "wilting": "wilt symptom",
        "wilt": "wilt disease symptom",
        "dry": "leaf drying symptom",
    }

    for word, expansion in symptom_terms.items():

        if word in lower:
            expansions.append(expansion)

    # Farming action expansion
    action_terms = {
        "what do": "recommended action precautions management",
        "what should i do": "recommended action precautions management",
        "how to control": "disease pest management control",
        "medicine": "treatment management precaution",
        "prevent": "prevention precaution",
    }

    for word, expansion in action_terms.items():

        if word in lower:
            expansions.append(expansion)

    # Season expansion
    season_terms = [
        "kharif",
        "rabi",
        "zaid",
        "summer",
        "winter",
        "monsoon"
    ]

    for season in season_terms:

        if season in lower:
            expansions.append(
                f"{season} season crop risk"
            )

    if expansions:

        query = (
            query
            + " "
            + " ".join(expansions)
        )

    return query


def process_query(query: str) -> dict:
    """
    Process a farmer question before RAG retrieval.
    """

    original_query = query

    retrieval_query = expand_farming_query(
        query
    )

    return {
        "original_query": original_query,
        "retrieval_query": retrieval_query
    }


if __name__ == "__main__":

    test_questions = [
        "rice leaf yelow what do",
        "paddy leaf turning yellow",
        "rice infection rainy season",
        "what medicine for leaf spot",
    ]

    print("=" * 70)
    print("FARMER QUERY UNDERSTANDING TEST")
    print("=" * 70)

    for question in test_questions:

        result = process_query(
            question
        )

        print("\n" + "-" * 70)

        print(
            "Farmer question:"
        )

        print(
            result["original_query"]
        )

        print(
            "\nRetrieval query:"
        )

        print(
            result["retrieval_query"]
        )