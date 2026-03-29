# `typst2pptx`

Convert Typst presentations to PPTX.

## How it works

Compiles `.typ` to PDF via `typst` CLI, renders each page as an image, and packs them into a `.pptx` file. The result is not editable — each slide is a raster image.

## Requirements

- Python 3.12+
- [typst](https://github.com/typst/typst/releases) CLI available in `$PATH`

## Installation
```bash
pip install typst2pptx
```

## Usage
```bash
typst2pptx slides.typ                         # → slides.pptx next to input
typst2pptx slides.typ -o out/result.pptx      # explicit output path
typst2pptx slides.typ --dpi 220               # higher quality
typst2pptx slides.typ --typst-bin ~/bin/typst # custom typst path
```

## DPI guide

| DPI | Use case |
|-----|----------|
| 96  | Screen only |
| 150 | Default, good for most presentations |
| 220 | Small text, formulas, high-quality export |