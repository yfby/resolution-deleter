# resolution-deleter

Deletes images below a minimum resolution from a directory.

## Installation

```bash
uv pip install -e .
```

## Usage

```bash
# Delete images below 1920x1080 in the current directory
resolution-deleter

# Scan a specific directory
resolution-deleter ~/Pictures

# Use custom minimum dimensions
resolution-deleter --min-width 1280 --min-height 720
```

## Supported formats

`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`

## TODO

- [ ] video support
