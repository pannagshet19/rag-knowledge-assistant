from dataclasses import dataclass
from typing import Dict


@dataclass
class Document:
    text: str
    metadata: Dict[str, str]


@dataclass
class Section:
    title: str
    content: str


@dataclass
class Chunk:
    text: str
    metadata: Dict[str, str]