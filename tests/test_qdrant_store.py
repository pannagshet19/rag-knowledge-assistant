from app.vectorstore.qdrant_store import QdrantStore
from app.ingestion.models import Chunk


def test_add_vector():

    store = QdrantStore("test_collection")

    chunk = Chunk(
        text="Employees can take sick leave when they are ill.",
        metadata={"section": "Sick Leave"},
        document_id="test-document",
        chunk_index=0,
    )

    vector = [0.1] * 384

    store.add_vector(vector, chunk)

    count = store.client.count(
        collection_name="test_collection"
    ).count

    assert count == 1