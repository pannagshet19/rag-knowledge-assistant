from app.ingestion.models import Document, Chunk
from app.ingestion.document_repository import save_document, save_chunk
from app.database import get_connection


def test_save_document():
    document = Document(
        text="Test document",
        metadata={"source": "test"},
    )

    conn = get_connection()

    try:
        save_document(document)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT document_id, text, metadata FROM documents WHERE document_id = %s",
                (document.document_id,),
            )

            row = cur.fetchone()

        assert row is not None
        assert str(row[0]) == document.document_id
        assert row[1] == document.text
        assert row[2] == document.metadata

    finally:
        conn.close()


def test_save_chunk():
    document = Document(
        text="Test document",
        metadata={"source": "test"},
    )

    save_document(document)

    chunk = Chunk(
        text="Test chunk",
        metadata={"section": "test"},
        document_id=document.document_id,
        chunk_index=0,
    )

    save_chunk(chunk)

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT chunk_id, document_id, chunk_index, text, metadata
                FROM chunks
                WHERE chunk_id = %s
                """,
                (chunk.chunk_id,),
            )

            row = cur.fetchone()

        assert row is not None
        assert str(row[0]) == chunk.chunk_id
        assert str(row[1]) == chunk.document_id
        assert row[2] == 0
        assert row[3] == chunk.text
        assert row[4] == chunk.metadata

    finally:
        conn.close()
        