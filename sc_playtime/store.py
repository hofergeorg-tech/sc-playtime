"""Session-Speicher (SQLite). Eine Zeile pro Spielsitzung.

``game`` ist der Anzeigename aus den Einstellungen, ``channel`` bei Star
Citizen der Installationsordner (LIVE, PTU, HOTFIX, TECH-PREVIEW …), sonst leer.
``version`` ist der Spiel-Patch (z. B. ``4.3.1``), sofern er sich ermitteln ließ.
``reason`` sagt, wie das Spiel endete (Star Citizen, aus dem ``Game.log``):
``quit`` normal beendet, ``crash`` abgestürzt, ``server`` vom Server/Backend getrennt,
leer = unbekannt (andere Spiele, AFK-Pause, ältere Sessions).
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
    version: str = ""
    reason: str = ""


_COLUMNS = "id, game, channel, start, end, version, reason"


class Store:
    def __init__(self, path: Path) -> None:
        self._db = sqlite3.connect(str(path))
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS sessions ("
            " id INTEGER PRIMARY KEY,"
            " game TEXT NOT NULL,"
            " channel TEXT NOT NULL DEFAULT '',"
            " start REAL NOT NULL,"
            " end REAL NOT NULL,"
            " version TEXT NOT NULL DEFAULT '')"
        )
        # Datenbanken bis 1.3.x haben noch keine Versionsspalte, bis 1.4.x kein Session-Ende
        columns = {row[1] for row in self._db.execute("PRAGMA table_info(sessions)")}
        if "version" not in columns:
            self._db.execute("ALTER TABLE sessions ADD COLUMN version TEXT NOT NULL DEFAULT ''")
        if "reason" not in columns:
            self._db.execute("ALTER TABLE sessions ADD COLUMN reason TEXT NOT NULL DEFAULT ''")
        self._db.execute("CREATE INDEX IF NOT EXISTS idx_sessions_game ON sessions(game, start)")
        self._db.commit()

    def all(self) -> list[SessionRow]:
        rows = self._db.execute(f"SELECT {_COLUMNS} FROM sessions ORDER BY start")
        return [SessionRow(int(i), g, c, float(s), float(e), v, r) for i, g, c, s, e, v, r in rows]

    def set_reason(self, session_id: int, reason: str) -> None:
        self._db.execute("UPDATE sessions SET reason = ? WHERE id = ?", (reason, session_id))
        self._db.commit()

    def insert(self, rows: list[SessionRow]) -> None:
        """Fertige Sessions übernehmen (Zusammenführen mit einem anderen PC)."""
        self._db.executemany(
            "INSERT INTO sessions(game, channel, start, end, version, reason) VALUES (?, ?, ?, ?, ?, ?)",
            [(r.game, r.channel, r.start, r.end, r.version, r.reason) for r in rows],
        )
        self._db.commit()

    def open(self, game: str, channel: str, start: float, now: float, version: str = "") -> SessionRow:
        """Session anlegen oder die jüngste dieses Prozesslaufs fortsetzen.

        Nach einer AFK-Pause besteht ein Lauf aus mehreren Sessions; alle
        beginnen frühestens beim Prozessstart. Fortgesetzt wird die letzte,
        sonst würde eine frühere über die späteren hinweg verlängert.
        """
        row = self._db.execute(
            "SELECT id, channel, start, end, version, reason FROM sessions WHERE game = ? AND start > ?"
            " ORDER BY start DESC LIMIT 1",
            (game, start - RESUME_TOLERANCE_S),
        ).fetchone()
        if row:
            return SessionRow(int(row[0]), game, row[1], float(row[2]), float(row[3]), row[4], row[5])
        cur = self._db.execute(
            "INSERT INTO sessions(game, channel, start, end, version) VALUES (?, ?, ?, ?, ?)",
            (game, channel, start, now, version),
        )
        self._db.commit()
        return SessionRow(int(cur.lastrowid), game, channel, start, now, version)

    def touch(self, session_id: int, end: float) -> None:
        self._db.execute("UPDATE sessions SET end = ? WHERE id = ?", (end, session_id))
        self._db.commit()

    def update(self, session_id: int, start: float, end: float) -> None:
        self._db.execute("UPDATE sessions SET start = ?, end = ? WHERE id = ?", (start, end, session_id))
        self._db.commit()

    def delete(self, session_id: int) -> None:
        self._db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        self._db.commit()

    def backup(self, dest: Path) -> None:
        """Konsistente Kopie der Datenbank, auch während geschrieben wird."""
        target = sqlite3.connect(str(dest))
        try:
            self._db.backup(target)
        finally:
            target.close()

    def close(self) -> None:
        self._db.close()
