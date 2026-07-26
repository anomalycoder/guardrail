from guards.path_guard import validate_path


def read_file(path: str) -> str:

    file_path = validate_path(path)

    if not file_path.exists():
        raise FileNotFoundError("File does not exist.")

    if not file_path.is_file():
        raise ValueError("Not a file.")

    return file_path.read_text(encoding="utf-8")
