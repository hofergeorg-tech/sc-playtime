"""Tägliche Sicherung der Datenbank nach <Datenordner>/backups, rotierend."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

from .store import Store

KEEP = 7  # so viele Tagesstände bleiben liegen
PREFIX = "playtime-"


def backup_dir(data: Path) -> Path:
    path = data / "backups"
    path.mkdir(parents=True, exist_ok=True)
    return path


def run(store: Store, folder: Path, today: date, keep: int = KEEP, force: bool = False) -> Optional[Path]:
    """Sichert den heutigen Stand (einmal am Tag, mit ``force`` immer) und löscht alte.

    Gibt die neue Datei zurück, ``None`` wenn es heute schon eine gab.
    """
    target = folder / f"{PREFIX}{today.isoformat()}.db"
    made: Optional[Path] = None
    if force or not target.exists():
        tmp = target.with_suffix(".tmp")
        tmp.unlink(missing_ok=True)
        store.backup(tmp)
        tmp.replace(target)  # erst die fertige Datei sichtbar machen
        made = target
    for old in sorted(folder.glob(f"{PREFIX}*.db"), reverse=True)[keep:]:
        try:
            old.unlink()
        except OSError:
            pass
    return made
