import logging
import shutil
import subprocess
from importlib.metadata import PackageNotFoundError, version

logger = logging.getLogger(__name__)

_REQUIRED_PYTHON_PACKAGES = ["fitz", "pptx", "PIL"]
_PACKAGE_IMPORT_TO_DIST: dict[str, str] = {
    "fitz": "pymupdf",
    "pptx": "python-pptx",
    "PIL": "Pillow",
}


def check_typst(typst_bin: str) -> None:
    """
    Verify that the typst CLI is available on the system.

    Args:
        typst_bin (str): Path or name of the typst executable.

    Raises:
        RuntimeError: If typst is not found or fails to run.
    """
    if not shutil.which(typst_bin):
        raise RuntimeError(
            f"typst not found: '{typst_bin}'\n"
            "Install it from https://github.com/typst/typst/releases\n"
            "or via: cargo install typst-cli"
        )

    result = subprocess.run(
        [typst_bin, "--version"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"typst found but failed to run: {result.stderr.strip()}"
        )

    logger.debug("typst version: %s", result.stdout.strip())


def check_python_packages() -> None:
    """
    Verify that all required Python packages are installed.

    Raises:
        RuntimeError: If one or more packages are missing.
    """
    missing = []

    for import_name in _REQUIRED_PYTHON_PACKAGES:
        dist_name = _PACKAGE_IMPORT_TO_DIST[import_name]
        try:
            version(dist_name)
        except PackageNotFoundError:
            missing.append(dist_name)

    if missing:
        packages = " ".join(missing)
        raise RuntimeError(
            f"Missing required packages: {', '.join(missing)}\n"
            f"Install via: pip install {packages}"
        )


def check_all(typst_bin: str) -> None:
    """
    Run all dependency checks.

    Args:
        typst_bin (str): Path or name of the typst executable.

    Raises:
        RuntimeError: If any dependency is missing.
    """
    check_python_packages()
    check_typst(typst_bin)
