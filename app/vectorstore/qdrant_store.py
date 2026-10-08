from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class QdrantStore:

    def __init__(self, collection_name: str = "documents"):
        self.client = QdrantClient(path="./qdrant_data")
        self.collection_name = collection_name

        self._create_collection()

    def _create_collection(self):

        collections = self.client.get_collections().collections

        if self.collection_name not in [c.name for c in collections]:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

    def add_vector(self, vector, chunk):

        point = PointStruct(
            id=chunk.chunk_id,
            vector=vector,
            payload={
                "text": chunk.text,
                "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index,
                "metadata": chunk.metadata,
            },
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

    def search(self, query_vector, limit=3):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
        ).points

        return results