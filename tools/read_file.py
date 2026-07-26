from pathlib import Path


def read_file(path: str) -> str:
    """
    Reads a file and returns its contents.
    Security checks will be added later.
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError("File does not exist.")

    if not file_path.is_file():
        raise ValueError("Not a file.")

    return file_path.read_text(encoding="utf-8")
