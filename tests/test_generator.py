from app.llm.generator import RAGGenerator


class FakeResult:

    def __init__(self, text, section):

        self.payload = {
            "text": text,
            "metadata": {
                "section": section
            }
        }


def test_rag_generation():

    results = [
        FakeResult(
            "Employees receive 20 days of annual leave.",
            "Annual Leave"
        ),
        FakeResult(
            "Employees can take sick leave when they are ill.",
            "Sick Leave"
        ),
    ]

    generator = RAGGenerator()

    answer = generator.generate(
        "What happens when an employee is sick?",
        results
    )

    assert answer
    assert isinstance(answer, str)

    print("\nRAG Answer:", answer)