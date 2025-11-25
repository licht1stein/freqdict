# Project Context

## Purpose
Build a personal word frequency dictionary tool that:
1. Reads text from multiple file formats (txt, md, docx, pdf)
2. Cleans and normalizes text (removes punctuation, special characters, normalizes case)
3. Counts word frequencies
4. Exports results to CSV/JSON/Excel
5. Lemmatizes words to their dictionary form (Russian via pymorphy3)

Goal: A simple, local CLI tool for building frequency dictionaries from personal text collections.

## Tech Stack
- Python 3.13
- uv for running (inline script dependencies via PEP 723)
- pymorphy3 for Russian lemmatization
- python-docx for .docx parsing
- shell.nix for development environment (includes uv, python)
- .envrc with `use nix` for direnv auto-activation

## Core Features (v1)
- File parsing: txt, md, docx
- Text cleaning (punctuation, normalization)
- Russian lemmatization (pymorphy3)
- Word frequency counting
- CSV export

## CLI Usage
- `uv run freqdict.py <file>` — process single file
- `uv run freqdict.py <dir>` — recursively find all .txt/.md/.docx in directory
- `uv run freqdict.py .` — process current directory

## macOS Distribution
Target: non-technical user on Mac
- `install-mac.sh` — installs uv, freqdict.py, and the Quick Action
- `Freqdict Here.workflow` — Automator Quick Action for Finder context menu
- User runs `bash install-mac.sh`, then right-click folder → Quick Actions → Freqdict Here

## Project Conventions

### Code Style
TBD

### Architecture Patterns
- CLI-first approach
- Pipeline architecture: Read → Clean → Count → Export
- Pluggable parsers per file format

### Testing Strategy
TBD

### Git Workflow
TBD

## Domain Context
- Frequency dictionary: a list of words ranked by how often they appear
- Lemmatization: reducing inflected forms to base form (e.g., "бежал" → "бежать")
- Russian is highly inflected — lemmatization is essential for meaningful frequency counts

## Important Constraints
- Must work offline (no cloud dependencies)
- Privacy-friendly (texts stay local)
- Single-file script (all deps declared inline via PEP 723)

## External Dependencies
- pymorphy3 + pymorphy3-dicts-ru — Russian morphological analyzer
- python-docx — .docx file parsing
