from pathlib import Path
from config import SANDBOX_ROOT


def validate_path(path: str) -> Path:
    """
    Validate that the requested file is inside the sandbox.
    """

    requested = Path(path).resolve()
    sandbox = SANDBOX_ROOT.resolve()

    try:
        requested.relative_to(sandbox)
    except ValueError:
        raise PermissionError("Access outside sandbox is forbidden.")

    return requested
