from app.services.rag_service import RAGService


def test_rag_service():

    service = RAGService()

    result = service.ask(
        "What is the sick leave policy?"
    )

    assert result["answer"]
    assert isinstance(result["answer"], str)

    assert len(result["sources"]) > 0

    print("\nQuestion:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:

        print(
            f"\nSource {source['source_number']}"
        )

        print(
            f"Section: {source['section']}"
        )

        print(
            f"Chunk: {source['chunk_index']}"
        )

        print(
            f"Score: {source['score']:.4f}"
        )

        print(
            f"Text: {source['text']}"
        )

    assert "section" in result["sources"][0]
    assert "score" in result["sources"][0]