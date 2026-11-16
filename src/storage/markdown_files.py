"""Reading and writing generated Markdown files."""

from pathlib import Path

OUTPUT_DIR = Path("output")


def save_markdown(filename: str, markdown: str) -> Path:
    """Saves Markdown text into the output directory.

    Args:
        filename: Name of the file inside the output directory.
        markdown: Markdown content to write.

    Returns:
        The path of the written file.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    file_path = OUTPUT_DIR / filename
    file_path.write_text(markdown, encoding="utf-8")
    return file_path


def load_markdown(filename: str) -> str:
    """Loads Markdown text from the output directory.

    Args:
        filename: Name of the file inside the output directory.

    Returns:
        The file content.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    file_path = OUTPUT_DIR / filename
    return file_path.read_text(encoding="utf-8")
