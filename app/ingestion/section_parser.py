from typing import List

from app.ingestion.models import Section


def parse_sections(text: str) -> List[Section]:
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    if not paragraphs:
        return []

    sections = []

    current_title = None
    current_content = []

    for paragraph in paragraphs:
        if current_title is None:
            current_title = paragraph

        elif len(paragraph.split()) <= 5:
            if current_content:
                sections.append(
                    Section(
                        title=current_title,
                        content="\n\n".join(current_content),
                    )
                )

            current_title = paragraph
            current_content = []

        else:
            current_content.append(paragraph)

    if current_title is not None:
        sections.append(
            Section(
                title=current_title,
                content="\n\n".join(current_content),
            )
        )

    return sections