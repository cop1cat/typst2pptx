# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`typst2pptx` is a Python CLI tool that converts Typst presentations (`.typ`) to PowerPoint (`.pptx`) by: compiling `.typ` → PDF via the `typst` CLI, rendering each PDF page as a PNG using PyMuPDF, then packing the images into a PPTX. The output is non-editable (raster slides).

## Commands

All commands use `uv`:

```bash
uv sync --extra dev          # Install all dependencies including dev
uv run pytest                # Run tests (requires 80% coverage)
uv run pytest tests/test_foo.py::test_bar  # Run a single test
uv run ruff check .          # Lint
uv run ruff format .         # Format
uv run ruff format --check . # Check formatting without modifying
uv run mypy . --explicit-package-bases --cache-dir=/dev/null  # Type check
hatch build                  # Build wheel/sdist for PyPI
```

## Architecture

```
cli.py → dependencies.py → converter.py
              ↑                  ↑
           config.py          config.py
```

- **`cli.py`** — Typer-based CLI. Parses args (`input_file`, `--output`, `--dpi`, `--typst-bin`, `--verbose`), resolves output path, sets up logging, then calls `dependencies.check_all()` and `converter.convert()`.
- **`config.py`** — Pydantic `ConvertConfig` model. Validates `dpi` (72–600, default 150) and `typst_bin` (default `"typst"`).
- **`dependencies.py`** — Checks that the `typst` binary is available and that `pymupdf`, `python-pptx`, and `Pillow` are installed.
- **`converter.py`** — Three-stage pipeline:
  1. `_compile_typst()` — shells out to `typst compile` to produce PDF bytes
  2. `_pdf_to_images()` — renders PDF pages to PNG via PyMuPDF (`fitz`), scaling by `dpi/72`
  3. `_build_pptx()` — creates a PPTX with slide dimensions from the first page, inserting each PNG as a full-slide image

## Known Issues in the Codebase

- `tests.yml` and `ruff.toml` contain copy-paste references to `steam_fetcher` that should be `typst2pptx`.
- No tests exist yet (`tests/` directory is missing); the 80% coverage threshold in `pytest.ini` will need tests before CI passes.
