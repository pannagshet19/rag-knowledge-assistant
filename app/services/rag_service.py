from app.retrieval.retriever import Retriever
from app.llm.generator import RAGGenerator


class RAGService:

    def __init__(self):

        self.retriever = Retriever()
        self.generator = RAGGenerator()

    def ask(self, question: str, limit: int = 3):

        results = self.retriever.retrieve(
            question,
            limit=limit,
        )

        answer = self.generator.generate(
            question,
            results,
        )

        sources = []

        for index, result in enumerate(results, start=1):

            payload = result.payload

            metadata = payload.get(
                "metadata",
                {}
            )

            sources.append(
                {
                    "source_number": index,
                    "document_id": payload.get(
                        "document_id"
                    ),
                    "section": metadata.get(
                        "section",
                        "Unknown"
                    ),
                    "chunk_index": payload.get(
                        "chunk_index"
                    ),
                    "text": payload.get(
                        "text",
                        ""
                    ),
                    "score": result.score,
                }
            )

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
        }