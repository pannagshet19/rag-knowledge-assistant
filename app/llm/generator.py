from app.llm.client import GeminiClient
from app.llm.prompts import build_rag_prompt


class RAGGenerator:

    def __init__(self):

        self.llm = GeminiClient()

    def generate(self, question: str, results):

        prompt = build_rag_prompt(
            question=question,
            results=results,
        )

        answer = self.llm.generate(prompt)

        return answer