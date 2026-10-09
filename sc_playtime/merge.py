"""Sessions eines anderen PCs übernehmen (dessen ``playtime.db`` oder eine Sicherung daraus).

Doppeltes wird übersprungen: Eine Session gilt als schon vorhanden, wenn es für dasselbe
Spiel bereits eine gibt, die sich zeitlich mit ihr überschneidet – dasselbe Spiel läuft
nicht gleichzeitig auf zwei PCs. So kann man dieselbe Datei auch mehrmals übernehmen.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from .store import SessionRow


@dataclass(frozen=True)
class MergePlan:
    new: list[SessionRow]
    duplicates: int

    def games(self) -> list[str]:
        return sorted({r.game for r in self.new})


def read_sessions(path: Path) -> list[SessionRow]:
    """Sessions aus einer fremden Datenbank lesen (nur lesend; ältere Versionen ohne Patch/Ende gehen auch)."""
    db = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
    try:
        columns = {row[1] for row in db.execute("PRAGMA table_info(sessions)")}
        if not {"game", "start", "end"} <= columns:
            raise sqlite3.DatabaseError("keine SC-Playtime-Datenbank")
        pick = ", ".join(c if c in columns else "''" for c in ("game", "channel", "start", "end", "version", "reason"))
        return [SessionRow(0, g, c or "", float(s), float(e), v or "", r or "")
                for g, c, s, e, v, r in db.execute(f"SELECT {pick} FROM sessions ORDER BY start")]
    finally:
        db.close()


def _overlaps(a: SessionRow, b: SessionRow) -> bool:
    if a.game != b.game:
        return False
    if abs(a.start - b.start) < 1.0:  # auch Sessions ohne Länge erkennen
        return True
    return a.start < b.end and b.start < a.end


def plan(existing: Sequence[SessionRow], incoming: Iterable[SessionRow]) -> MergePlan:
    by_game: dict[str, list[SessionRow]] = {}
    for r in existing:
        by_game.setdefault(r.game, []).append(r)
    new: list[SessionRow] = []
    duplicates = 0
    for r in incoming:
        if r.end < r.start:
            continue
        known = by_game.setdefault(r.game, [])
        if any(_overlaps(r, k) for k in known):
            duplicates += 1
            continue
        known.append(r)
        new.append(r)
    return MergePlan(new, duplicates)
