"""Session-Speicher (SQLite). Eine Zeile pro Spielsitzung.

``game`` ist der Anzeigename aus den Einstellungen, ``channel`` bei Star
Citizen der Installationsordner (LIVE, PTU, HOTFIX, TECH-PREVIEW …), sonst leer.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

# Startet das Overlay neu, während das Spiel läuft, liefert die Prozess-
# Startzeit dieselbe Session — innerhalb dieser Toleranz wird sie fortgesetzt.
RESUME_TOLERANCE_S = 5.0


@dataclass
class SessionRow:
    id: int
    game: str
    channel: str
    start: float
    end: float


class Store:
    def __init__(self, path: Path) -> None:
        self._db = sqlite3.connect(str(path))
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS sessions ("
            " id INTEGER PRIMARY KEY,"
            " game TEXT NOT NULL,"
            " channel TEXT NOT NULL DEFAULT '',"
            " start REAL NOT NULL,"
            " end REAL NOT NULL)"
        )
        self._db.execute("CREATE INDEX IF NOT EXISTS idx_sessions_game ON sessions(game, start)")
        self._db.commit()

    def all(self) -> list[SessionRow]:
        rows = self._db.execute("SELECT id, game, channel, start, end FROM sessions ORDER BY start")
        return [SessionRow(int(i), g, c, float(s), float(e)) for i, g, c, s, e in rows]

    def open(self, game: str, channel: str, start: float, now: float) -> SessionRow:
        """Session anlegen oder eine mit gleicher Startzeit fortsetzen."""
        row = self._db.execute(
            "SELECT id, end FROM sessions WHERE game = ? AND ABS(start - ?) < ?"
            " ORDER BY start DESC LIMIT 1",
            (game, start, RESUME_TOLERANCE_S),
        ).fetchone()
        if row:
            return SessionRow(int(row[0]), game, channel, start, float(row[1]))
        cur = self._db.execute(
            "INSERT INTO sessions(game, channel, start, end) VALUES (?, ?, ?, ?)",
            (game, channel, start, now),
        )
        self._db.commit()
        return SessionRow(int(cur.lastrowid), game, channel, start, now)

    def touch(self, session_id: int, end: float) -> None:
        self._db.execute("UPDATE sessions SET end = ? WHERE id = ?", (end, session_id))
        self._db.commit()

    def close(self) -> None:
        self._db.close()
