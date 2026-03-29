import logging
import subprocess
from pathlib import Path
from typing import Annotated

import typer
from typst2pptx.config import ConvertConfig
from typst2pptx.converter import convert
from typst2pptx.dependencies import check_all

app = typer.Typer(
    name="typst2pptx",
    help="Convert Typst presentations to PPTX.",
    add_completion=False,
)


def _setup_logging(verbose: bool) -> None:
    """
    Настраивает уровень логирования.

    Args:
        verbose (bool): Если True — выводит DEBUG сообщения.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=level,
    )


def _resolve_output(input_path: Path, output: Path | None) -> Path:
    """
    Определяет путь для выходного файла.

    Args:
        input_path (Path): Путь к исходному .typ файлу.
        output (Path | None): Явно указанный путь или None.

    Returns:
        Path: Итоговый путь к .pptx файлу.
    """
    if output is not None:
        return output
    return input_path.with_suffix(".pptx")


@app.command()
def main(
    input_file: Annotated[Path, typer.Argument(help="Path to .typ file")],
    output_file: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Output .pptx path (default: same dir as input)",
        ),
    ] = None,
    dpi: Annotated[
        int, typer.Option("--dpi", "-d", help="Render resolution (72-600)")
    ] = 150,
    typst_bin: Annotated[
        str, typer.Option("--typst-bin", help="Path to typst executable")
    ] = "typst",
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Enable debug output")
    ] = False,
) -> None:
    """
    Конвертирует .typ файл в .pptx через PDF-рендер.
    """
    _setup_logging(verbose)

    try:
        check_all(typst_bin)
    except RuntimeError as e:
        typer.echo(f"Dependency error: {e}", err=True)
        raise typer.Exit(code=1) from e

    config = ConvertConfig(dpi=dpi, typst_bin=typst_bin)
    output_path = _resolve_output(input_file, output_file)

    try:
        convert(input_file, output_path, config)
        typer.echo(f"✓ {output_path}")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1) from e
    except subprocess.CalledProcessError as e:
        typer.echo(f"Typst compilation failed:\n{e.stderr}", err=True)
        raise typer.Exit(code=1) from e
