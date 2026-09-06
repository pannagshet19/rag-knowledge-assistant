from typing import List

from app.ingestion.models import Section


def chunk_sections(
    sections: List[Section],
    chunk_size: int,
    overlap: int,
) -> List[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    for section in sections:
        section_text = section.title

        if section.content:
            section_text += "\n\n" + section.content

        # Section fits completely in one chunk.
        if len(section_text) <= chunk_size:
            chunks.append(section_text)
            continue

        # Section is larger than chunk_size.
        paragraphs = section.content.split("\n\n")

        current_chunk = section.title

        for paragraph in paragraphs:
            candidate = current_chunk + "\n\n" + paragraph

            if len(candidate) <= chunk_size:
                current_chunk = candidate

            else:
                chunks.append(current_chunk)

                # Take the last `overlap` characters
                # from the previous chunk.
                overlap_text = (
                    current_chunk[-overlap:]
                    if overlap > 0
                    else ""
                )

                current_chunk = (
                    section.title
                    + "\n\n"
                    + overlap_text
                    + paragraph
                )

        if current_chunk:
            chunks.append(current_chunk)

    return chunks