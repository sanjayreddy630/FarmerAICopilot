import re
from typing import List, Dict


def clean_text(text: str) -> str:
    """
    Clean PDF text and remove repeated dataset template sections.
    """

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove repeated template sections.
    remove_patterns = [
        r"RECOMMENDED FIELDS.*?(?=\n[A-Z][A-Z +\-&/]{2,}:?\s*\n|\Z)",
        r"FARMER / RAG QUESTIONS.*?(?=\n[A-Z][A-Z +\-&/]{2,}:?\s*\n|\Z)",
        r"EXAMPLE DATA RECORD.*?(?=\n[A-Z][A-Z +\-&/]{2,}:?\s*\n|\Z)",
    ]

    for pattern in remove_patterns:
        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

    # Remove repeated dataset title.
    text = re.sub(
        r"FARMING DATASET",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Normalize spaces.
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive blank lines.
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def detect_metadata(text: str) -> Dict[str, str]:
    """
    Extract useful farming metadata.
    """

    metadata = {
        "crop": "",
        "season": "",
        "growth_stage": "",
        "problem": "",
        "technology": "",
    }

    lower = text.lower()

    # Seasons
    seasons = [
        "kharif",
        "rabi",
        "zaid",
        "perennial"
    ]

    for season in seasons:
        if season in lower:
            metadata["season"] = season.title()
            break

    # Crops
    crops = [
        "rice",
        "wheat",
        "maize",
        "cotton",
        "tomato",
        "chilli",
        "groundnut",
        "soybean",
        "sugarcane",
        "potato",
        "onion",
        "pulses",
        "millets",
        "vegetables",
        "fruits",
    ]

    found_crops = [
        crop
        for crop in crops
        if crop in lower
    ]

    if found_crops:
        metadata["crop"] = ", ".join(
            crop.title()
            for crop in found_crops
        )

    # Growth stages
    stages = [
        "germination",
        "seedling",
        "vegetative",
        "flowering",
        "fruiting",
        "maturity",
        "harvest",
    ]

    found_stages = [
        stage
        for stage in stages
        if stage in lower
    ]

    if found_stages:
        metadata["growth_stage"] = ", ".join(
            stage.title()
            for stage in found_stages
        )

    # Problems
    problem_terms = [
        "disease",
        "pest",
        "infection",
        "leaf curl",
        "leaf spot",
        "blight",
        "blast",
        "rust",
        "wilt",
        "root rot",
        "weed",
        "nutrient deficiency",
    ]

    found_problems = [
        term
        for term in problem_terms
        if term in lower
    ]

    if found_problems:
        metadata["problem"] = ", ".join(
            found_problems
        )

    # Modern farming technologies
    technologies = [
        "drip irrigation",
        "sprinkler irrigation",
        "fertigation",
        "soil sensors",
        "soil-moisture sensors",
        "automated irrigation",
        "weather stations",
        "iot",
        "drones",
        "satellite imagery",
        "satellite remote sensing",
        "gis",
        "gps",
        "precision farming",
        "precision seeding",
        "variable-rate technology",
        "ai",
        "machine learning",
        "computer vision",
        "greenhouse",
        "polyhouse",
        "hydroponics",
        "aeroponics",
        "vertical farming",
        "solar irrigation",
        "robotics",
        "smart pest traps",
        "climate-smart farming",
    ]

    for technology in technologies:
        if technology in lower:
            metadata["technology"] = technology.title()
            break

    return metadata


def create_chunks(
    pages: List[Dict],
    max_chars: int = 1800,
    overlap: int = 250
) -> List[Dict]:
    """
    Create structure-aware chunks from PDF pages.

    Each chunk contains:
    - chunk_id
    - page
    - text
    - metadata
    """

    chunks = []

    for page in pages:

        page_number = page["page"]

        text = clean_text(
            page["text"]
        )

        if not text:
            continue

        # Split around section headings.
        sections = re.split(
            r"\n(?=[A-Z][A-Z +\-&/]{2,}:?\s*\n)",
            text
        )

        current_chunk = ""

        for section in sections:

            section = section.strip()

            if not section:
                continue

            # Save current chunk when it becomes too large.
            if (
                current_chunk
                and len(current_chunk)
                + len(section)
                + 2
                > max_chars
            ):

                chunk_text = current_chunk.strip()

                chunks.append({
                    "chunk_id": (
                        f"page_{page_number}_"
                        f"chunk_{len(chunks) + 1}"
                    ),
                    "page": page_number,
                    "text": chunk_text,
                    "metadata": detect_metadata(
                        chunk_text
                    ),
                })

                # Preserve overlap.
                current_chunk = (
                    current_chunk[-overlap:]
                    + "\n\n"
                    + section
                )

            else:

                if current_chunk:
                    current_chunk += (
                        "\n\n" + section
                    )
                else:
                    current_chunk = section

        # Save remaining chunk.
        if current_chunk.strip():

            chunk_text = current_chunk.strip()

            chunks.append({
                "chunk_id": (
                    f"page_{page_number}_"
                    f"chunk_{len(chunks) + 1}"
                ),
                "page": page_number,
                "text": chunk_text,
                "metadata": detect_metadata(
                    chunk_text
                ),
            })

    return chunks


if __name__ == "__main__":

    from ingestion.loader import load_pdf

    pages = load_pdf()

    chunks = create_chunks(
        pages
    )

    print("=" * 70)
    print("CLEANED ADVANCED RAG CHUNKING TEST")
    print("=" * 70)

    print(
        f"Pages loaded  : {len(pages)}"
    )

    print(
        f"Chunks created: {len(chunks)}"
    )

    if chunks:

        print("\nFIRST CHUNK")
        print("-" * 70)

        print(
            f"Chunk ID: "
            f"{chunks[0]['chunk_id']}"
        )

        print(
            f"Page: "
            f"{chunks[0]['page']}"
        )

        print(
            f"Metadata: "
            f"{chunks[0]['metadata']}"
        )

        print("\nText:")
        print(
            chunks[0]["text"][:1500]
        )