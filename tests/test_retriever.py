from app.embeddings.embedder import Embedder
from app.ingestion.models import Chunk
from app.vectorstore.qdrant_store import QdrantStore
from app.retrieval.retriever import Retriever


def test_retrieval():

    collection_name = "retrieval_test"

    embedder = Embedder()
    store = QdrantStore(collection_name)

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
        Chunk(
            text="Employees can work remotely up to three days per week.",
            metadata={"section": "Remote Work"},
            document_id="test-document",
            chunk_index=2,
        ),
    ]

    vectors = embedder.embed_chunks(chunks)

    for vector, chunk in zip(vectors, chunks):
        store.add_vector(vector, chunk)

    query = "What happens when an employee is sick?"

    query_vector = embedder.embed_text(query)

    results = store.search(
        query_vector=query_vector,
        limit=2,
    )

    assert len(results) == 2

    texts = [result.payload["text"] for result in results]

    assert any("sick leave" in text.lower() for text in texts)