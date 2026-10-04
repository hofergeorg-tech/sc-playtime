"""Verfolgt die konfigurierten Spiele (EXE-Namen) und schreibt daraus Sessions.

AFK-Erkennung (optional): Gibt es länger als ``afk_s`` keine Eingabe am PC,
endet die Session beim letzten Tastendruck. Sobald wieder eine Eingabe kommt
und das Spiel noch läuft, beginnt eine neue Session.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Iterable, Optional

from . import process
from .store import SessionRow, Store

# So oft wird das Session-Ende in die DB geschrieben. Stürzt das Overlay ab,
# gehen höchstens so viele Sekunden verloren.
HEARTBEAT_S = 30.0
CHANNEL_ORDER = ("LIVE", "PTU", "EPTU", "HOTFIX", "TECH-PREVIEW")


@dataclass(frozen=True)
class Game:
    name: str
    exe: str


def sort_channels(channels: Iterable[str]) -> list[str]:
    def key(c: str) -> tuple[int, str]:
        return (CHANNEL_ORDER.index(c) if c in CHANNEL_ORDER else len(CHANNEL_ORDER), c)

    return sorted(set(channels), key=key)


class Tracker:
    def __init__(
        self,
        store: Store,
        games: Iterable[Game],
        find: Callable[[Iterable[str]], dict[str, int]] = process.find_processes,
        start_time: Callable[[int], Optional[float]] = process.process_start_time,
        image_path: Callable[[int], Optional[str]] = process.process_image_path,
        version: Callable[[int], str] = process.process_version,
        idle: Callable[[], Optional[float]] = process.idle_seconds,
        afk_s: float = 0.0,
    ) -> None:
        self._store = store
        self._find = find
        self._start_time = start_time
        self._image_path = image_path
        self._version = version
        self._idle = idle
        self.afk_s = afk_s  # 0 = AFK-Erkennung aus
        self._games: list[Game] = list(games)
        self._rows: list[SessionRow] = store.all()
        self._live: dict[str, SessionRow] = {}  # game name → laufende Session
        self._paused: dict[str, SessionRow] = {}  # game name → letzte Session vor der AFK-Pause
        self._flushed: dict[str, float] = {}

    def set_games(self, games: Iterable[Game]) -> None:
        self._games = list(games)
        names = {g.name for g in self._games}
        for name in list(self._live):
            if name not in names:
                self._close(name, time.time())
        for name in list(self._paused):
            if name not in names:
                del self._paused[name]

    def poll(self, now: Optional[float] = None) -> None:
        now = time.time() if now is None else now
        pids = self._find(g.exe for g in self._games)
        idle = self._idle() if self.afk_s > 0 else None
        away = idle is not None and idle >= self.afk_s
        for game in self._games:
            pid = pids.get(game.exe.lower())
            if pid is None:
                self._paused.pop(game.name, None)
                if game.name in self._live:
                    self._close(game.name, now)
                continue

            live = self._live.get(game.name)
            if away:
                if live is not None:
                    # Session endet bei der letzten Eingabe, nicht erst jetzt
                    self._close(game.name, max(live.start, now - idle), extend=False)
                    self._paused[game.name] = live
                elif game.name not in self._paused:
                    # Spiel läuft schon, aber niemand sitzt davor: noch nichts
                    # speichern, nur Channel/Patch für die spätere Session merken
                    self._paused[game.name] = SessionRow(
                        0, game.name, process.channel_from_path(self._image_path(pid)),
                        now - idle, now - idle, self._version(pid),
                    )
                continue

            if live is None:
                before = self._paused.pop(game.name, None)
                if before is not None:
                    # zurück vom AFK: neue Session ab der ersten Eingabe
                    start = now - idle if idle is not None else now
                    live = self._open(game.name, pid, now, start=max(start, before.end),
                                      channel=before.channel, version=before.version)
                else:
                    live = self._open(game.name, pid, now)
            live.end = max(live.end, now)
            if now - self._flushed[game.name] >= HEARTBEAT_S:
                self._store.touch(live.id, live.end)
                self._flushed[game.name] = now

    def _open(self, name: str, pid: int, now: float, start: Optional[float] = None,
              channel: Optional[str] = None, version: Optional[str] = None) -> SessionRow:
        if start is None:
            start = min(self._start_time(pid) or now, now)
        if channel is None:
            channel = process.channel_from_path(self._image_path(pid))
        if version is None:
            version = self._version(pid)
        row = self._store.open(name, channel, start, now, version)
        live = next((r for r in self._rows if r.id == row.id), None)
        if live is None:
            live = row
            self._rows.append(live)
        self._live[name] = live
        self._flushed[name] = now
        return live

    def _close(self, name: str, end: float, extend: bool = True) -> None:
        live = self._live.pop(name)
        live.end = max(live.end, end) if extend else end
        self._store.touch(live.id, live.end)

    def flush(self) -> None:
        now = time.time()
        for live in self._live.values():
            live.end = max(live.end, now)
            self._store.touch(live.id, live.end)

    # --- Bearbeiten -----------------------------------------------------------

    def is_live(self, session_id: int) -> bool:
        return any(r.id == session_id for r in self._live.values())

    def update_session(self, session_id: int, start: float, end: float) -> None:
        """Start/Ende einer abgeschlossenen Session korrigieren."""
        if self.is_live(session_id) or end <= start:
            raise ValueError("laufende Session oder Ende vor Start")
        self._store.update(session_id, start, end)
        for r in self._rows:
            if r.id == session_id:
                r.start, r.end = start, end
        self._rows.sort(key=lambda r: r.start)

    def delete_session(self, session_id: int) -> None:
        if self.is_live(session_id):
            raise ValueError("laufende Session")
        self._store.delete(session_id)
        self._rows = [r for r in self._rows if r.id != session_id]

    # --- Abfragen für die Anzeige -------------------------------------------

    def running(self) -> list[str]:
        """Laufende Spiele (auch in der AFK-Pause) in Konfigurationsreihenfolge."""
        return [g.name for g in self._games if g.name in self._live or g.name in self._paused]

    def is_afk(self, game: str) -> bool:
        return game in self._paused

    def live_channel(self, game: str) -> Optional[str]:
        live = self._live.get(game) or self._paused.get(game)
        return live.channel if live else None

    def channels(self, game: str) -> list[str]:
        return sort_channels(r.channel for r in self._rows if r.game == game and r.channel)

    def rows(self, game: Optional[str] = None) -> list[SessionRow]:
        """Alle Sessions (Kopien), ältere zuerst; optional nur ein Spiel."""
        return [SessionRow(r.id, r.game, r.channel, r.start, r.end, r.version)
                for r in self._rows if game is None or r.game == game]

    def _match(self, game: str, channel: str) -> list[SessionRow]:
        return [r for r in self._rows if r.game == game and (not channel or r.channel == channel)]

    def sessions(self, game: str, channel: str = "") -> list[tuple[float, float]]:
        return [(r.start, r.end) for r in self._match(game, channel)]

    def versioned(self, game: str, channel: str = "") -> list[tuple[str, float, float]]:
        return [(r.version, r.start, r.end) for r in self._match(game, channel)]

    def current_duration(self, game: str, channel: str = "") -> float:
        """Laufende Session, sonst Dauer der letzten (für die Offline-Anzeige)."""
        live = self._live.get(game)
        if live is not None and (not channel or live.channel == channel):
            return max(0.0, time.time() - live.start)
        rows = self._match(game, channel)
        return rows[-1].end - rows[-1].start if rows else 0.0
