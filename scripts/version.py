# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""
Version bump script for freqdict.
Usage: uv run scripts/version.py <new_version>
Example: uv run scripts/version.py 0.2
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Pattern for URLs in README.md and install-mac.sh
URL_VERSION_PATTERN = re.compile(r"(freqdict/v)(\d+\.\d+)")
# Pattern for VERSION constant in freqdict.py
CONST_VERSION_PATTERN = re.compile(r'(VERSION = ")(\d+\.\d+)(")')


def get_current_version() -> str | None:
    """Get current version from freqdict.py."""
    script = ROOT / "freqdict.py"
    match = CONST_VERSION_PATTERN.search(script.read_text())
    return match.group(2) if match else None


def update_version_in_files(new_version: str) -> list[Path]:
    """Update version in all files. Returns list of modified files."""
    modified = []

    # Update VERSION constant in freqdict.py
    script = ROOT / "freqdict.py"
    content = script.read_text()
    new_content = CONST_VERSION_PATTERN.sub(rf'\g<1>{new_version}\g<3>', content)
    if new_content != content:
        script.write_text(new_content)
        modified.append(script)

    # Update URLs in README.md and install-mac.sh
    for path in [ROOT / "README.md", ROOT / "install-mac.sh"]:
        content = path.read_text()
        new_content = URL_VERSION_PATTERN.sub(rf"\g<1>{new_version}", content)
        if new_content != content:
            path.write_text(new_content)
            modified.append(path)

    return modified


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return result."""
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, cwd=ROOT)


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <new_version>")
        print(f"Example: {sys.argv[0]} 0.2")
        sys.exit(1)

    new_version = sys.argv[1]
    tag = f"v{new_version}"
    current = get_current_version()

    print(f"Current version: {current}")
    print(f"New version: {new_version}")
    print()

    # Update files
    modified = update_version_in_files(new_version)
    if not modified:
        print("No files were modified. Version may already be set.")
        sys.exit(1)

    print(f"Updated {len(modified)} file(s):")
    for path in modified:
        print(f"  - {path.relative_to(ROOT)}")
    print()

    # Git operations
    run(["git", "add"] + [str(p) for p in modified])
    run(["git", "commit", "-m", f"Bump version to {new_version}"])

    # Delete old tag if exists (locally and remotely)
    run(["git", "tag", "-d", tag], check=False)
    run(["git", "push", "origin", f":refs/tags/{tag}"], check=False)

    # Create new tag
    run(["git", "tag", tag])

    # Push commit and tag
    run(["git", "push", "origin", "master", tag])

    print()
    print(f"Done! Version {new_version} released.")
    print(f"Install URL: https://raw.githubusercontent.com/licht1stein/freqdict/{tag}/install-mac.sh")


if __name__ == "__main__":
    main()
