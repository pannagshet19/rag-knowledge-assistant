from app.llm.client import GeminiClient


def test_gemini():

    llm = GeminiClient()

    response = llm.generate(
        "Explain what Retrieval Augmented Generation is in one sentence."
    )

    assert response
    assert isinstance(response, str)

    print("\nGemini:", response)