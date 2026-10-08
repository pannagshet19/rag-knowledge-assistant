from app.ingestion.text_loader import load_text
from app.ingestion.section_parser import parse_sections
from app.ingestion.chunker import chunk_sections
from app.ingestion.document_repository import save_document_with_chunks
from app.embeddings.embedder import Embedder
from app.vectorstore.qdrant_store import QdrantStore


def main():

    # -----------------------------
    # 1. Load document
    # -----------------------------

    document = load_text("data/sample_document.txt")

    print(f"Document ID: {document.document_id}")

    # -----------------------------
    # 2. Parse document into sections
    # -----------------------------

    sections = parse_sections(document.text)

    print(f"Number of sections: {len(sections)}")

    # -----------------------------
    # 3. Create chunks
    # -----------------------------

    chunks = chunk_sections(
        sections,
        document_id=str(document.document_id),
        chunk_size=200,
        overlap=0,
    )

    print(f"Number of chunks: {len(chunks)}")

    # -----------------------------
    # 4. Save document + chunks
    #    to PostgreSQL
    # -----------------------------

    save_document_with_chunks(
        document,
        chunks,
    )

    print("Document and chunks saved to PostgreSQL.")

    # -----------------------------
    # 5. Generate embeddings
    # -----------------------------

    embedder = Embedder()

    vectors = embedder.embed_chunks(chunks)

    print(f"Generated {len(vectors)} embeddings.")

    # -----------------------------
    # 6. Store embeddings in Qdrant
    # -----------------------------

    vector_store = QdrantStore()

    for vector, chunk in zip(vectors, chunks):

        vector_store.add_vector(
            vector,
            chunk,
        )

    print("Embeddings stored in Qdrant.")

    print("\nRAG ingestion completed successfully.")


if __name__ == "__main__":
    main()