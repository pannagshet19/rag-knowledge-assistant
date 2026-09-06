from app.ingestion.text_loader import load_text
from app.ingestion.section_parser import parse_sections
from app.ingestion.chunker import chunk_sections


def main():
    document = load_text("data/sample_document.txt")

    sections = parse_sections(document.text)

    chunks = chunk_sections(
        sections,
        chunk_size=200,
        overlap=0,
    )

    print(f"Number of sections: {len(sections)}")
    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i + 1} ---")
        print(chunk)


if __name__ == "__main__":
    main()