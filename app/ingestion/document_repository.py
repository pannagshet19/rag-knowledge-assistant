from typing import List

from psycopg.types.json import Jsonb

from app.database import get_connection
from app.ingestion.models import Document, Chunk


def save_document(document: Document):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (document_id, text, metadata)
                VALUES (%s, %s, %s)
                """,
                (
                    document.document_id,
                    document.text,
                    Jsonb(document.metadata),
                ),
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def save_chunk(chunk: Chunk):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chunks (
                    chunk_id,
                    document_id,
                    chunk_index,
                    text,
                    metadata
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    chunk.chunk_id,
                    chunk.document_id,
                    chunk.chunk_index,
                    chunk.text,
                    Jsonb(chunk.metadata),
                ),
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def save_document_with_chunks(
    document: Document,
    chunks: List[Chunk],
):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (document_id, text, metadata)
                VALUES (%s, %s, %s)
                """,
                (
                    document.document_id,
                    document.text,
                    Jsonb(document.metadata),
                ),
            )

            for chunk in chunks:
                cur.execute(
                    """
                    INSERT INTO chunks (
                        chunk_id,
                        document_id,
                        chunk_index,
                        text,
                        metadata
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        chunk.chunk_id,
                        chunk.document_id,
                        chunk.chunk_index,
                        chunk.text,
                        Jsonb(chunk.metadata),
                    ),
                )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
