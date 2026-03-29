# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-03-29

### Changed

- Set up deploy to pypi when creating tags at main branch

---

## [0.1.0] - 2026-03-29

### Added

- CLI command `typst2pptx` with `--output`, `--dpi` (72–600, default 150), `--typst-bin`, and `--verbose` flags
- Three-stage conversion pipeline: `.typ` → PDF via `typst` CLI → per-page PNG via PyMuPDF → `.pptx` via python-pptx
- Test suite covering `config`, `dependencies`, `converter`, and `cli` modules
