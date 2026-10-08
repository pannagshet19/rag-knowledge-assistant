from app.embeddings.embedder import Embedder
from app.vectorstore.qdrant_store import QdrantStore


class Retriever:

    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = QdrantStore()

    def retrieve(self, question: str, limit: int = 3):

        query_vector = self.embedder.embed_text(question)

        results = self.vector_store.search(
            query_vector=query_vector,
            limit=limit,
        )

        return results