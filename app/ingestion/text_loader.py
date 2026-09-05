from pathlib import Path

from app.ingestion.models import Document


def load_text(file_path: str) -> Document:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    text = path.read_text(encoding="utf-8")

    return Document(
        text=text,
        metadata={
            "source": str(path),
            "file_type": path.suffix,
        },
    )