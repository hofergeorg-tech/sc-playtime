"""Wie endete eine Star-Citizen-Sitzung? Aus dem ``Game.log`` – nur lesend.

Star Citizen schreibt beim Beenden eine Zeile ``<SystemQuit> CSystem::Quit invoked with -
cause=…, reason=…, exitCode=…``. Mit "Quit via console command" bzw. "User closed the
application" hat der Spieler selbst beendet; andere Gründe ("Back-end services are
unresponsive" …) kommen vom Server. Bei einem Absturz fehlt die Zeile, stattdessen übergibt
das Spiel an seinen Crash-Collector. Jeder Spielstart landet danach in ``logbackups``
(``Game Build(…) 09 Oct 26 (07 43 28).log``), daraus lassen sich auch ältere Sessions einordnen.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path, PureWindowsPath
from typing import Iterable, Optional, Sequence

QUIT, CRASH, SERVER = "quit", "crash", "server"
REASONS = (QUIT, CRASH, SERVER)

TAIL_BYTES = 64 * 1024
# Ein Log gehört zu der Session, die (fast) zur selben Zeit endete
MATCH_TOLERANCE_S = 300.0

_SYSTEM_QUIT = re.compile(r"<SystemQuit>.*?reason=(?P<reason>[^,\n]*)")
_PLAYER_QUITS = ("quit via console command", "user closed the application")
_CRASH_MARKERS = ("crash info collector", "crash related data")


def reason_from_log(text: str) -> str:
    """``quit`` / ``crash`` / ``server`` aus dem Ende eines Game.log, ``""`` wenn nicht erkennbar."""
    quit_match = None
    for quit_match in _SYSTEM_QUIT.finditer(text):
        pass
    lower = text.lower()
    crash_at = max(lower.rfind(m) for m in _CRASH_MARKERS)
    if crash_at >= 0 and (quit_match is None or crash_at > quit_match.start()):
        return CRASH
    if quit_match is not None:
        reason = quit_match.group("reason").strip().lower()
        return QUIT if reason in _PLAYER_QUITS else SERVER
    return ""


def read_tail(path: Path, size: int = TAIL_BYTES) -> str:
    with path.open("rb") as f:
        f.seek(0, os.SEEK_END)
        f.seek(max(0, f.tell() - size))
        return f.read().decode("utf-8", errors="replace")


def channel_dir(image_path: Optional[str]) -> Optional[Path]:
    """``…\\StarCitizen\\LIVE\\Bin64\\StarCitizen.exe`` → ``…\\StarCitizen\\LIVE`` (nur wenn es ihn gibt)."""
    if not image_path:
        return None
    p = PureWindowsPath(image_path)
    if p.parent.name.lower() != "bin64":
        return None
    folder = Path(str(p.parent.parent))
    return folder if folder.is_dir() else None


def reason_for_dir(folder: Path, since: float) -> str:
    """Ende des Spiels, das gerade in ``folder`` lief (``Game.log`` jünger als ``since``)."""
    log = folder / "Game.log"
    try:
        if log.stat().st_mtime < since:
            return ""  # Log eines früheren Laufs
        return reason_from_log(read_tail(log))
    except OSError:
        return ""


def default_dirs() -> list[Path]:
    """Channel-Ordner der Standardinstallation (LIVE, PTU, …), für die Nachträge beim Start."""
    if sys.platform != "win32":
        return []
    base = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Roberts Space Industries" / "StarCitizen"
    try:
        return [d for d in base.iterdir() if (d / "logbackups").is_dir() or (d / "Game.log").is_file()]
    except OSError:
        return []


def backfill(rows: Sequence, folders: Iterable[Path]) -> list[tuple[int, str]]:
    """Sessions ohne Ende-Angabe aus den gesicherten Logs einordnen → ``[(id, reason)]``.

    Ein Log passt zur Session desselben Channels, deren Ende am nächsten an seinem
    letzten Schreibzeitpunkt liegt (höchstens :data:`MATCH_TOLERANCE_S` entfernt).
    Gelesen wird nur, wenn überhaupt eine Session in Frage kommt.
    """
    open_rows = [r for r in rows if not r.reason and r.id]
    updates: dict[int, str] = {}
    for folder in {Path(f) for f in folders}:
        channel = folder.name.upper()
        candidates = [r for r in open_rows if r.channel == channel]
        if not candidates:
            continue
        try:
            logs = list((folder / "logbackups").glob("*.log"))
        except OSError:
            continue
        for log in logs:
            try:
                ended = log.stat().st_mtime
            except OSError:
                continue
            near = [r for r in candidates if abs(r.end - ended) <= MATCH_TOLERANCE_S and r.id not in updates]
            if not near:
                continue
            try:
                reason = reason_from_log(read_tail(log))
            except OSError:
                continue
            if reason:
                updates[min(near, key=lambda r: abs(r.end - ended)).id] = reason
    return list(updates.items())
