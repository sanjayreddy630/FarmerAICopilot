import json
import re
from pathlib import Path

import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


INDEX_DIR = Path("rag/index")

FAISS_PATH = INDEX_DIR / "farming.index"
CHUNKS_PATH = INDEX_DIR / "chunks.json"

MODEL_NAME = "all-MiniLM-L6-v2"


# =========================================================
# AGRICULTURAL QUERY EXPANSION
# =========================================================

SYNONYMS = {
    "yellow": [
        "yellow",
        "yellowing",
        "yellow leaves",
        "leaf yellowing",
        "chlorosis",
        "pale leaves",
    ],

    "rice": [
        "rice",
        "paddy",
        "paddy rice",
    ],

    "leaf": [
        "leaf",
        "leaves",
        "foliar",
        "foliage",
    ],

    "disease": [
        "disease",
        "infection",
        "symptom",
        "pathogen",
    ],

    "spot": [
        "spot",
        "leaf spot",
        "lesion",
        "leaf lesion",
    ],

    "treatment": [
        "treatment",
        "management",
        "control",
        "precaution",
        "action",
        "recommendation",
    ],

    "precaution": [
        "precaution",
        "prevention",
        "prevent",
        "management",
        "control",
    ],

    "water": [
        "water",
        "irrigation",
        "moisture",
        "drainage",
    ],

    "nutrient": [
        "nutrient",
        "nutrition",
        "fertilizer",
        "nitrogen",
        "deficiency",
    ],

    "pest": [
        "pest",
        "insect",
        "insect pest",
        "damage",
    ],
}


def normalize_text(text: str) -> str:

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def expand_query(query: str) -> str:

    normalized = normalize_text(query)

    terms = [normalized]

    for key, synonyms in SYNONYMS.items():

        if key in normalized:

            terms.extend(synonyms)

    # Common farming phrase expansion

    if (
        "yellow" in normalized
        and (
            "rice" in normalized
            or "paddy" in normalized
        )
    ):

        terms.extend([
            "rice leaf yellowing",
            "paddy leaf yellowing",
            "rice yellow leaves",
            "paddy yellow leaves",
            "rice crop yellowing",
            "leaf discoloration",
            "nutrient deficiency",
            "water stress",
            "disease symptoms",
            "crop management",
            "precautions",
        ])

    if "what should i do" in normalized:

        terms.extend([
            "recommended action",
            "management",
            "precautions",
            "control",
            "treatment",
        ])

    return " ".join(terms)


# =========================================================
# HYBRID RETRIEVER
# =========================================================

class HybridRetriever:

    def __init__(self):

        print("Loading farming knowledge base...")

        # ---------------------------------------------
        # FAISS
        # ---------------------------------------------

        self.index = faiss.read_index(
            str(FAISS_PATH)
        )

        # ---------------------------------------------
        # CHUNKS
        # ---------------------------------------------

        with open(
            CHUNKS_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            self.chunks = json.load(file)

        # ---------------------------------------------
        # EMBEDDING MODEL
        # ---------------------------------------------

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        # ---------------------------------------------
        # BM25 CORPUS
        # ---------------------------------------------

        self.corpus = []

        for chunk in self.chunks:

            text = normalize_text(
                chunk.get("text", "")
            )

            self.corpus.append(
                text.split()
            )

        self.bm25 = BM25Okapi(
            self.corpus
        )

        print(
            f"Knowledge base loaded: "
            f"{len(self.chunks)} chunks"
        )


    # =====================================================
    # DENSE SEARCH
    # =====================================================

    def dense_search(
        self,
        query: str,
        top_k: int = 10
    ):

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index < 0:
                continue

            if index >= len(self.chunks):
                continue

            chunk = self.chunks[index].copy()

            chunk["dense_score"] = float(
                score
            )

            results.append(chunk)

        return results


    # =====================================================
    # BM25 SEARCH
    # =====================================================

    def keyword_search(
        self,
        query: str,
        top_k: int = 10
    ):

        expanded_query = expand_query(
            query
        )

        tokens = normalize_text(
            expanded_query
        ).split()

        scores = self.bm25.get_scores(
            tokens
        )

        top_indices = np.argsort(
            scores
        )[::-1][:top_k]

        results = []

        for index in top_indices:

            if scores[index] <= 0:
                continue

            chunk = self.chunks[index].copy()

            chunk["bm25_score"] = float(
                scores[index]
            )

            results.append(chunk)

        return results


    # =====================================================
    # HYBRID SEARCH
    # =====================================================

    def hybrid_search(
        self,
        query: str,
        top_k: int = 10
    ):

        expanded_query = expand_query(
            query
        )

        print(
            "\nExpanded retrieval query:"
        )

        print(
            expanded_query
        )


        dense_results = self.dense_search(
            expanded_query,
            top_k=top_k * 3
        )

        keyword_results = self.keyword_search(
            expanded_query,
            top_k=top_k * 3
        )


        combined = {}


        # ---------------------------------------------
        # DENSE RANK
        # ---------------------------------------------

        for rank, result in enumerate(
            dense_results
        ):

            chunk_id = result[
                "chunk_id"
            ]

            combined.setdefault(
                chunk_id,
                {
                    "chunk": result,
                    "score": 0.0
                }
            )

            combined[
                chunk_id
            ]["score"] += (
                0.55 / (rank + 1)
            )


        # ---------------------------------------------
        # BM25 RANK
        # ---------------------------------------------

        for rank, result in enumerate(
            keyword_results
        ):

            chunk_id = result[
                "chunk_id"
            ]

            combined.setdefault(
                chunk_id,
                {
                    "chunk": result,
                    "score": 0.0
                }
            )

            combined[
                chunk_id
            ]["score"] += (
                0.45 / (rank + 1)
            )


        # ---------------------------------------------
        # SORT
        # ---------------------------------------------

        ranked = sorted(
            combined.values(),
            key=lambda x: x["score"],
            reverse=True
        )


        final_results = []


        for item in ranked[:top_k]:

            chunk = item[
                "chunk"
            ].copy()

            chunk[
                "hybrid_score"
            ] = round(
                item["score"],
                4
            )

            final_results.append(
                chunk
            )


        return final_results


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    retriever = HybridRetriever()


    queries = [

        "My rice leaves are turning yellow. What should I do?",

        "paddy leaf yellowing",

        "rice infection rainy season",

        "what precautions should be taken for rice disease",

    ]


    for query in queries:

        print("\n")
        print("=" * 70)

        print(
            "QUERY:"
        )

        print(
            query
        )

        print("=" * 70)


        results = retriever.hybrid_search(
            query,
            top_k=5
        )


        for i, result in enumerate(
            results,
            start=1
        ):

            print("\n" + "-" * 70)

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

            print("\nText:")

            print(
                result.get(
                    "text",
                    ""
                )[:700]
            )