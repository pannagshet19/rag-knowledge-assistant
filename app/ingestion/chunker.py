from typing import List

from app.ingestion.models import Chunk, Section


def chunk_sections(
    sections: List[Section],
    document_id: str,
    chunk_size: int,
    overlap: int,
) -> List[Chunk]:

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
            chunks.append(
                Chunk(
                    text=section_text,
                    metadata={
                        "section": section.title,
                    },
                    document_id=document_id,
                    chunk_index=len(chunks),
                )
            )

            continue

        # Section is larger than chunk_size.
        # Section is split by paragraphs while keeping title.

        paragraphs = section.content.split("\n\n")

        current_chunk = section.title

        for paragraph in paragraphs:

            candidate = current_chunk + "\n\n" + paragraph

            if len(candidate) <= chunk_size:
                current_chunk = candidate

            else:
                chunks.append(
                    Chunk(
                        text=current_chunk,
                        metadata={
                            "section": section.title,
                        },
                        document_id=document_id,
                        chunk_index=len(chunks),
                    )
                )

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
            chunks.append(
                Chunk(
                    text=current_chunk,
                    metadata={
                        "section": section.title,
                    },
                    document_id=document_id,
                    chunk_index=len(chunks),
                )
            )

    return chunks