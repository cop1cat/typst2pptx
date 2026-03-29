from importlib.metadata import PackageNotFoundError
from unittest.mock import MagicMock, patch

import pytest

from typst2pptx.dependencies import (
    check_all,
    check_python_packages,
    check_typst,
)


def test_check_typst_not_found() -> None:
    with (
        patch("typst2pptx.dependencies.shutil.which", return_value=None),
        pytest.raises(RuntimeError, match="typst not found"),
    ):
        check_typst("typst")


def test_check_typst_fails_to_run() -> None:
    with patch(
        "typst2pptx.dependencies.shutil.which", return_value="/usr/bin/typst"
    ):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "error"
        with patch(
            "typst2pptx.dependencies.subprocess.run", return_value=mock_result
        ), pytest.raises(RuntimeError, match="failed to run"):
            check_typst("typst")


def test_check_typst_success() -> None:
    with patch(
        "typst2pptx.dependencies.shutil.which", return_value="/usr/bin/typst"
    ):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "typst 0.12.0"
        with patch(
            "typst2pptx.dependencies.subprocess.run", return_value=mock_result
        ):
            check_typst("typst")  # должен не бросать исключений


def test_check_python_packages_all_present() -> None:
    with patch("typst2pptx.dependencies.version", return_value="1.0"):
        check_python_packages()  # должен не бросать исключений


def test_check_python_packages_one_missing() -> None:
    def fake_version(dist_name: str) -> str:
        if dist_name == "pymupdf":
            raise PackageNotFoundError(dist_name)
        return "1.0"

    with (
        patch("typst2pptx.dependencies.version", side_effect=fake_version),
        pytest.raises(RuntimeError, match="pymupdf"),
    ):
        check_python_packages()


def test_check_python_packages_multiple_missing() -> None:
    with patch(
        "typst2pptx.dependencies.version",
        side_effect=PackageNotFoundError("pkg"),
    ), pytest.raises(RuntimeError, match="Missing required packages"):
        check_python_packages()


def test_check_all_calls_both() -> None:
    with (
        patch("typst2pptx.dependencies.check_python_packages") as mock_pkgs,
        patch("typst2pptx.dependencies.check_typst") as mock_typst,
    ):
        check_all("typst")
        mock_pkgs.assert_called_once()
        mock_typst.assert_called_once_with("typst")
