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

VERSION = "0.10"
SUPPORTED_EXTENSIONS = {".txt", ".md", ".docx", ".doc"}
WORD_PATTERN = re.compile(r"[а-яёА-ЯЁa-zA-Z]+")

# Russian stopwords (prepositions, conjunctions, particles, pronouns)
STOPWORDS = {
    # Prepositions
    "в", "на", "с", "к", "из", "у", "о", "от", "по", "за", "для", "до", "без",
    "при", "через", "над", "под", "между", "про", "об", "перед", "около",
    # Conjunctions
    "и", "а", "но", "или", "да", "либо", "то", "ни", "что", "чтобы", "если",
    "когда", "как", "потому", "поэтому", "хотя", "однако", "также", "тоже",
    # Particles
    "не", "бы", "же", "ли", "вот", "даже", "уже", "ещё", "еще", "только",
    "лишь", "именно", "ведь", "разве", "неужели", "пусть", "пускай",
    # Pronouns
    "я", "ты", "он", "она", "оно", "мы", "вы", "они", "себя", "свой",
    "мой", "твой", "наш", "ваш", "его", "её", "их", "этот", "тот", "такой",
    "какой", "который", "чей", "весь", "сам", "самый", "каждый", "любой",
    "другой", "иной", "некоторый", "никакой", "ничей",
    # Common verbs (auxiliary)
    "быть", "мочь", "хотеть", "должный", "стать", "являться",
    # Other common words
    "это", "так", "там", "тут", "здесь", "где", "куда", "откуда", "почему",
    "зачем", "очень", "можно", "нужно", "надо", "нет", "есть", "был", "будет",
}


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
    # Use UTF-8 mapping to properly handle Cyrillic and other non-Latin text
    result = subprocess.run(
        ["antiword", "-m", "UTF-8.txt", str(path)],
        capture_output=True,
        check=True,
    )
    return result.stdout.decode("utf-8")


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
    # Filter out Word temp/lock files (e.g., ~$document.doc)
    files = [f for f in files if not f.name.startswith("~$")]
    return sorted(set(files))


def tokenize(text: str) -> list[str]:
    """Extract words from text."""
    return WORD_PATTERN.findall(text.lower())


def lemmatize(words: list[str], morph: pymorphy3.MorphAnalyzer) -> list[str]:
    """Lemmatize words using pymorphy3, filtering out stopwords."""
    lemmas = []
    for word in words:
        lemma = morph.parse(word)[0].normal_form
        if lemma not in STOPWORDS:
            lemmas.append(lemma)
    return lemmas


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
    print(f"Freqdict v{VERSION}", file=sys.stderr)

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
