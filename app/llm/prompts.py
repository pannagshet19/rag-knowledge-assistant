def build_rag_prompt(question: str, results) -> str:

    context_parts = []

    for index, result in enumerate(results, start=1):

        text = result.payload.get("text", "")

        metadata = result.payload.get("metadata", {})

        section = metadata.get("section", "Unknown Section")

        context_parts.append(
            f"[Source {index} - {section}]\n{text}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an AI knowledge assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use information that is not present in the context.
2. Do not invent or hallucinate information.
3. If the context does not contain the answer, say:
   "I could not find the answer in the provided documents."
4. Mention the relevant source number when possible.

CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    return prompt