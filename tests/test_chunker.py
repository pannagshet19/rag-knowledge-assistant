from app.embeddings.embedder import Embedder
from app.ingestion.models import Chunk


def test_embedding_generation():

    embedder = Embedder()

    vector = embedder.embed_text(
        "Employees can take sick leave when they are ill."
    )

    assert isinstance(vector, list)
    assert len(vector) == 384


def test_chunk_embeddings():

    embedder = Embedder()

    chunks = [
        Chunk(
            text="Employees receive 20 days of annual leave.",
            metadata={"section": "Annual Leave"},
            document_id="test-document",
            chunk_index=0,
        ),
        Chunk(
            text="Employees can take sick leave when they are ill.",
            metadata={"section": "Sick Leave"},
            document_id="test-document",
            chunk_index=1,
        ),
    ]

    vectors = embedder.embed_chunks(chunks)

    assert len(vectors) == 2
    assert len(vectors[0]) == 384
    assert len(vectors[1]) == 384