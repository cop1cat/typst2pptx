import fitz
import pytest


@pytest.fixture
def minimal_pdf_bytes() -> bytes:
    doc = fitz.open()
    doc.new_page(width=595, height=842)
    return doc.tobytes() # type: ignore[no-any-return]
