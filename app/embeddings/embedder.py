from sentence_transformers import SentenceTransformer


class Embedder:

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        vector = self.model.encode(text)
        return vector.tolist()

    def embed_chunks(self, chunks):
        texts = [chunk.text for chunk in chunks]

        vectors = self.model.encode(texts)

        return [vector.tolist() for vector in vectors]