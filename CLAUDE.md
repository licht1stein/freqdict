# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Freqdict is a word frequency dictionary builder for Russian texts. It processes text files (.txt, .md, .docx), lemmatizes words using pymorphy3, and outputs a CSV with word frequencies.

## Development Environment

Uses Nix + direnv for environment setup:
```bash
direnv allow  # activates shell.nix with uv
```

## Commands

```bash
# Run the main script
uv run freqdict.py <file_or_directory>
uv run freqdict.py .  # process current directory

# Release a new version (updates URLs, commits, tags, pushes)
uv run scripts/version.py 0.4
```

## Architecture

Single-file script (`freqdict.py`) with inline PEP 723 dependencies. Pipeline:
1. `find_files()` — recursively collect .txt/.md/.docx files
2. `extract_text()` — dispatch to format-specific parsers
3. `tokenize()` — regex extraction of words
4. `lemmatize()` — pymorphy3 reduces to base forms
5. `write_csv()` — output sorted by frequency

macOS distribution via `install-mac.sh` which downloads the script and installs an Automator Quick Action (`Freqdict Here.workflow`).

## Versioning

Version is embedded in URLs in `README.md` and `install-mac.sh`. Use `scripts/version.py` to bump — it updates files, commits, tags, and pushes.

<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->