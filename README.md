# Freqdict

Build a word frequency dictionary from your texts with Russian lemmatization.

## Features

- Supports `.txt`, `.md`, `.org`, `.doc`, `.docx` files
- Russian lemmatization (pymorphy3)
- Recursively processes directories
- Exports to CSV

## macOS Installation (one-liner)

```bash
curl -fsSL https://raw.githubusercontent.com/licht1stein/freqdict/v0.15/install-mac.sh | sh
```

The install script will:
1. Install [uv](https://docs.astral.sh/uv/) (Python package runner) if not present
2. Install [antiword](http://www.winfield.demon.nl/) via Homebrew (for `.doc` support)
3. Download `freqdict.py` to `~/.local/share/freqdict/`
4. Install a Finder Quick Action to `~/Library/Services/`

After installation, right-click any folder in Finder and select:
**Quick Actions → Freqdict Here**

The output `frequency_dict.csv` will be created in that folder.

## CLI Usage

Requires [uv](https://docs.astral.sh/uv/).

```bash
# Process a single file
uv run freqdict.py document.txt

# Process a directory (recursive)
uv run freqdict.py ./my-texts/

# Process current directory
uv run freqdict.py .
```

Output: `frequency_dict.csv` with columns `lemma,frequency`, sorted by frequency descending.

## Example Output

```csv
lemma,frequency
быть,42
который,28
мочь,15
говорить,12
...
```
