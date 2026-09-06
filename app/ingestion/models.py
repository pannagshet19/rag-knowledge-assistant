from dataclasses import dataclass, field
from typing import Dict
from uuid import uuid4


@dataclass
class Document:

    text: str

    metadata: Dict[str, str]

    document_id: str = field(
        default_factory=lambda: str(uuid4())
    )


@dataclass
class Section:

    title: str

    content: str


@dataclass
class Chunk:

    text: str

    metadata: Dict[str, str]

    chunk_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    document_id: str = ""

    chunk_index: int = 0