from app.embeddings.embedder import Embedder


def test_embedding_generation():

    embedder = Embedder()

    vector = embedder.embed_text(
        "Employees can take sick leave when they are ill."
    )

    assert isinstance(vector, list)
    assert len(vector) == 384