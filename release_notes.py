"""Release-Text aus den Changelogs für eine Version (vom CI-Workflow genutzt).

    python release_notes.py 1.3.0 > notes.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = "https://github.com/hofergeorg-tech/sc-playtime/blob/main"


def section(changelog: Path, version: str) -> str:
    """Text unter ``## [version]`` bis zur nächsten Versionsüberschrift."""
    text = changelog.read_text(encoding="utf-8")
    match = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.S | re.M)
    if not match:
        raise SystemExit(f"{changelog.name}: kein Abschnitt für {version}")
    return match.group(1).strip()


def main() -> None:
    version = sys.argv[1].lstrip("v")
    print(f"## 🇩🇪 Deutsch\n\n{section(ROOT / 'CHANGELOG.md', version)}\n")
    print(f"## 🇬🇧 English\n\n{section(ROOT / 'CHANGELOG.en.md', version)}\n")
    print("---\n")
    print("**Windows:** `SC-Playtime.exe` · **Linux:** `SC-Playtime-linux-x86_64` (`chmod +x`)\n")
    print(f"[Hilfe]({REPO}/HILFE.md) · [Help]({REPO}/HELP.md)")


if __name__ == "__main__":
    main()
