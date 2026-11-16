"""Text extraction from uploaded hiring documents (PDF, Word, plain text)."""

import io


def _extract_pdf_text(file_bytes: bytes) -> str:
    """Extracts text from every page of a PDF.

    Args:
        file_bytes: Raw bytes of the PDF file.

    Returns:
        The text of all non-empty pages, separated by blank lines.
    """
    # Imported here so backend startup does not pay for the PDF library.
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(file_bytes))
    page_texts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            page_texts.append(page_text)
    return "\n\n".join(page_texts)


def _extract_word_text(file_bytes: bytes) -> str:
    """Extracts paragraph text from a Word document.

    Falls back to decoding the raw bytes as UTF-8 when the file cannot be
    parsed as a .docx (for example a legacy .doc file).

    Args:
        file_bytes: Raw bytes of the Word file.

    Returns:
        The non-blank paragraphs joined by newlines.
    """
    try:
        # Imported here so backend startup does not pay for the Word library.
        import docx

        document = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception:
        return file_bytes.decode("utf-8", errors="ignore")


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extracts plain text from an uploaded file based on its extension.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        filename: Original file name, used only to detect the extension.

    Returns:
        The extracted text with surrounding whitespace removed. Unknown
        extensions are decoded as UTF-8 text.
    """
    extension = filename.lower().split(".")[-1]

    if extension == "pdf":
        text = _extract_pdf_text(file_bytes)
    elif extension in ("docx", "doc"):
        text = _extract_word_text(file_bytes)
    else:
        # txt, md and anything unknown are treated as plain text.
        text = file_bytes.decode("utf-8", errors="ignore")

    return text.strip()
