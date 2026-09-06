import pytest

from app.ingestion.chunker import chunk_sections
from app.ingestion.models import Section


def test_section_that_fits_in_one_chunk():
    sections = [
        Section(
            title="Annual Leave",
            content="Employees receive 20 days of annual leave.",
        )
    ]

    chunks = chunk_sections(
        sections,
        chunk_size=200,
        overlap=0,
    )

    assert len(chunks) == 1
    assert "Annual Leave" in chunks[0]
    assert "20 days" in chunks[0]


def test_multiple_sections_create_multiple_chunks():
    sections = [
        Section(
            title="Annual Leave",
            content="Employees receive 20 days of annual leave.",
        ),
        Section(
            title="Sick Leave",
            content="Employees can take sick leave when they are ill.",
        ),
    ]

    chunks = chunk_sections(
        sections,
        chunk_size=200,
        overlap=0,
    )

    assert len(chunks) == 2
    assert "Annual Leave" in chunks[0]
    assert "Sick Leave" in chunks[1]


def test_section_title_stays_with_content():
    sections = [
        Section(
            title="Remote Work",
            content="Employees may work remotely up to 3 days per week.",
        )
    ]

    chunks = chunk_sections(
        sections,
        chunk_size=200,
        overlap=0,
    )

    assert len(chunks) == 1
    assert chunks[0].startswith("Remote Work")
    assert "3 days per week" in chunks[0]


def test_invalid_chunk_size():
    sections = [
        Section(
            title="Annual Leave",
            content="Employees receive 20 days of annual leave.",
        )
    ]

    with pytest.raises(ValueError):
        chunk_sections(
            sections,
            chunk_size=0,
            overlap=0,
        )


def test_negative_overlap():
    sections = [
        Section(
            title="Annual Leave",
            content="Employees receive 20 days of annual leave.",
        )
    ]

    with pytest.raises(ValueError):
        chunk_sections(
            sections,
            chunk_size=200,
            overlap=-1,
        )


def test_overlap_cannot_equal_chunk_size():
    sections = [
        Section(
            title="Annual Leave",
            content="Employees receive 20 days of annual leave.",
        )
    ]

    with pytest.raises(ValueError):
        chunk_sections(
            sections,
            chunk_size=100,
            overlap=100,
        )


def test_chunks_have_overlap():
    sections = [
        Section(
            title="Annual Leave",
            content=(
                "Employees receive 20 days of annual leave.\n\n"
                "Employees should submit annual leave requests at least "
                "3 days before the requested leave date."
            ),
        )
    ]

    chunks = chunk_sections(
        sections,
        chunk_size=100,
        overlap=30,
    )

    assert len(chunks) > 1

    # The last 30 characters of the first chunk
    # should appear in the second chunk.
    assert chunks[0][-30:] in chunks[1]