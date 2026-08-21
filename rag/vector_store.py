import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from ingestion.chunker import create_chunks
from ingestion.loader import load_pdf


# --------------------------------------------------
# Paths
# --------------------------------------------------

INDEX_DIR = Path("rag/index")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

FAISS_PATH = INDEX_DIR / "farming.index"
CHUNKS_PATH = INDEX_DIR / "chunks.json"


# --------------------------------------------------
# Embedding model
# --------------------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"


def build_vector_store():

    print("=" * 70)
    print("BUILDING FARMING VECTOR DATABASE")
    print("=" * 70)

    # 1. Load PDF
    print("\n[1/5] Loading PDF...")

    pages = load_pdf()

    print(f"Pages loaded: {len(pages)}")

    # 2. Create chunks
    print("\n[2/5] Creating chunks...")

    chunks = create_chunks(pages)

    print(f"Chunks created: {len(chunks)}")

    # 3. Prepare text
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # 4. Load embedding model
    print("\n[3/5] Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print(f"Model loaded: {MODEL_NAME}")

    # 5. Create embeddings
    print("\n[4/5] Creating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    print(f"Embedding shape: {embeddings.shape}")

    # --------------------------------------------------
    # FAISS index
    # --------------------------------------------------

    print("\n[5/5] Building FAISS index...")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    # Save index
    faiss.write_index(
        index,
        str(FAISS_PATH)
    )

    # Save chunks + metadata
    with open(
        CHUNKS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\n" + "=" * 70)
    print("VECTOR DATABASE READY")
    print("=" * 70)

    print(f"Total vectors : {index.ntotal}")
    print(f"Vector size   : {dimension}")
    print(f"FAISS index   : {FAISS_PATH}")
    print(f"Chunks file   : {CHUNKS_PATH}")


if __name__ == "__main__":
    build_vector_store()