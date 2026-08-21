from pathlib import Path
from pypdf import PdfReader


PDF_PATH = Path("data/farming_dataset.pdf")


def load_pdf(pdf_path: Path = PDF_PATH):
    """Extract the farming PDF page by page."""

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page": page_number,
            "text": text.strip()
        })

    return pages


if __name__ == "__main__":
    pages = load_pdf()

    print(f"Total pages loaded: {len(pages)}")

    for page in pages[:2]:
        print("\n" + "=" * 70)
        print(f"PAGE {page['page']}")
        print("=" * 70)
        print(page["text"][:1000])