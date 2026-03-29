import subprocess
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from typst2pptx.cli import _resolve_output, app

runner = CliRunner()


# --- _resolve_output ---


def test_resolve_output_none() -> None:
    result = _resolve_output(Path("/tmp/slides.typ"), None)
    assert result == Path("/tmp/slides.pptx")


def test_resolve_output_explicit() -> None:
    explicit = Path("/out/presentation.pptx")
    result = _resolve_output(Path("/tmp/slides.typ"), explicit)
    assert result == explicit


# --- CLI ---


def test_cli_success(tmp_path: Path) -> None:
    typ_file = tmp_path / "slides.typ"
    typ_file.write_text("")

    with (
        patch("typst2pptx.cli.check_all"),
        patch("typst2pptx.cli.convert"),
    ):
        result = runner.invoke(app, [str(typ_file)])

    assert result.exit_code == 0
    assert "✓" in result.output


def test_cli_default_output_path(tmp_path: Path) -> None:
    typ_file = tmp_path / "slides.typ"
    typ_file.write_text("")
    expected_output = tmp_path / "slides.pptx"

    with (
        patch("typst2pptx.cli.check_all"),
        patch("typst2pptx.cli.convert") as mock_convert,
    ):
        runner.invoke(app, [str(typ_file)])

    _, call_args, _ = mock_convert.mock_calls[0]
    assert call_args[1] == expected_output


def test_cli_custom_output_path(tmp_path: Path) -> None:
    typ_file = tmp_path / "slides.typ"
    typ_file.write_text("")
    custom_output = tmp_path / "custom.pptx"

    with (
        patch("typst2pptx.cli.check_all"),
        patch("typst2pptx.cli.convert") as mock_convert,
    ):
        runner.invoke(app, [str(typ_file), "--output", str(custom_output)])

    _, call_args, _ = mock_convert.mock_calls[0]
    assert call_args[1] == custom_output


def test_cli_dependency_error(tmp_path: Path) -> None:
    typ_file = tmp_path / "slides.typ"
    typ_file.write_text("")

    with patch(
        "typst2pptx.cli.check_all", side_effect=RuntimeError("typst not found")
    ):
        result = runner.invoke(app, [str(typ_file)])

    assert result.exit_code == 1
    assert "Dependency error" in result.output


def test_cli_file_not_found(tmp_path: Path) -> None:
    typ_file = tmp_path / "slides.typ"
    typ_file.write_text("")

    with (
        patch("typst2pptx.cli.check_all"),
        patch(
            "typst2pptx.cli.convert",
            side_effect=FileNotFoundError("slides.typ not found"),
        ),
    ):
        result = runner.invoke(app, [str(typ_file)])

    assert result.exit_code == 1
    assert "Error" in result.output


def test_cli_typst_compile_error(tmp_path: Path) -> None:
    typ_file = tmp_path / "slides.typ"
    typ_file.write_text("")

    with (
        patch("typst2pptx.cli.check_all"),
        patch(
            "typst2pptx.cli.convert",
            side_effect=subprocess.CalledProcessError(
                1, "typst", stderr="syntax error"
            ),
        ),
    ):
        result = runner.invoke(app, [str(typ_file)])

    assert result.exit_code == 1
    assert "Typst compilation failed" in result.output


def test_cli_verbose_flag(tmp_path: Path) -> None:
    typ_file = tmp_path / "slides.typ"
    typ_file.write_text("")

    with (
        patch("typst2pptx.cli.check_all"),
        patch("typst2pptx.cli.convert"),
    ):
        result = runner.invoke(app, [str(typ_file), "--verbose"])

    assert result.exit_code == 0
