# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pymorphy3",
#     "pymorphy3-dicts-ru",
#     "python-docx",
# ]
# ///
"""
Frequency dictionary builder for Russian texts.
Usage: uv run freqdict.py <file_or_directory> [...]
"""

import csv
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pymorphy3
from docx import Document

SUPPORTED_EXTENSIONS = {".txt", ".md", ".docx", ".doc"}
WORD_PATTERN = re.compile(r"[а-яёА-ЯЁa-zA-Z]+")


def extract_text_from_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_text_from_docx(path: Path) -> str:
    doc = Document(path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def extract_text_from_doc(path: Path) -> str:
    """Extract text from legacy .doc files using antiword."""
    if not shutil.which("antiword"):
        raise RuntimeError(
            f"Cannot read {path.name}: antiword not installed.\n"
            "Install with: brew install antiword (macOS) or apt install antiword (Linux)"
        )
    result = subprocess.run(
        ["antiword", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".txt", ".md"}:
        return extract_text_from_txt(path)
    elif ext == ".docx":
        return extract_text_from_docx(path)
    elif ext == ".doc":
        return extract_text_from_doc(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def find_files(paths: list[Path]) -> list[Path]:
    """Recursively find all supported files from given paths."""
    files = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
        elif path.is_dir():
            for ext in SUPPORTED_EXTENSIONS:
                files.extend(path.rglob(f"*{ext}"))
    return sorted(set(files))


def tokenize(text: str) -> list[str]:
    """Extract words from text."""
    return WORD_PATTERN.findall(text.lower())


def lemmatize(words: list[str], morph: pymorphy3.MorphAnalyzer) -> list[str]:
    """Lemmatize words using pymorphy3."""
    return [morph.parse(word)[0].normal_form for word in words]


def build_frequency_dict(files: list[Path]) -> Counter:
    """Build frequency dictionary from files."""
    morph = pymorphy3.MorphAnalyzer()
    counter: Counter = Counter()

    for file in files:
        print(f"Processing: {file}", file=sys.stderr)
        text = extract_text(file)
        words = tokenize(text)
        lemmas = lemmatize(words, morph)
        counter.update(lemmas)

    return counter


def write_csv(counter: Counter, output_path: Path) -> None:
    """Write frequency dictionary to CSV."""
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lemma", "frequency"])
        for lemma, freq in counter.most_common():
            writer.writerow([lemma, freq])


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run freqdict.py <file_or_directory> [...]", file=sys.stderr)
        sys.exit(1)

    input_paths = [Path(arg) for arg in sys.argv[1:]]
    files = find_files(input_paths)

    if not files:
        print("No supported files found (.txt, .md, .doc, .docx)", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(files)} file(s)", file=sys.stderr)

    counter = build_frequency_dict(files)

    output_path = Path("frequency_dict.csv")
    write_csv(counter, output_path)

    print(f"Wrote {len(counter)} unique lemmas to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
