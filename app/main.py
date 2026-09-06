from app.ingestion.text_loader import load_text
from app.ingestion.section_parser import parse_sections
from app.ingestion.chunker import chunk_sections
from app.ingestion.document_repository import save_document_with_chunks


def main():
    document = load_text("data/sample_document.txt")

    sections = parse_sections(document.text)

    chunks = chunk_sections(
        sections,
        document_id=document.document_id,
        chunk_size=200,
        overlap=0,
    )

    save_document_with_chunks(document, chunks)

    print(f"Document ID: {document.document_id}")
    print(f"Number of sections: {len(sections)}")
    print(f"Number of chunks: {len(chunks)}")

    for chunk in chunks:
        print(f"\n--- Chunk {chunk.chunk_index} ---")
        print(f"Chunk ID: {chunk.chunk_id}")
        print(f"Document ID: {chunk.document_id}")
        print(chunk.text)


if __name__ == "__main__":
    main()