"""Verfolgt die konfigurierten Spiele (EXE-Namen) und schreibt daraus Sessions."""

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
    ) -> None:
        self._store = store
        self._find = find
        self._start_time = start_time
        self._image_path = image_path
        self._games: list[Game] = list(games)
        self._rows: list[SessionRow] = store.all()
        self._live: dict[str, SessionRow] = {}  # game name → laufende Session
        self._flushed: dict[str, float] = {}

    def set_games(self, games: Iterable[Game]) -> None:
        self._games = list(games)
        for name in list(self._live):
            if all(g.name != name for g in self._games):
                self._close(name, time.time())

    def poll(self, now: Optional[float] = None) -> None:
        now = time.time() if now is None else now
        pids = self._find(g.exe for g in self._games)
        for game in self._games:
            pid = pids.get(game.exe.lower())
            live = self._live.get(game.name)
            if pid is not None and live is None:
                start = min(self._start_time(pid) or now, now)
                channel = process.channel_from_path(self._image_path(pid))
                row = self._store.open(game.name, channel, start, now)
                live = next((r for r in self._rows if r.id == row.id), None)
                if live is None:
                    live = row
                    self._rows.append(live)
                self._live[game.name] = live
                self._flushed[game.name] = now
            if live is None:
                continue
            live.end = max(live.end, now)
            if pid is None:
                self._close(game.name, now)
            elif now - self._flushed[game.name] >= HEARTBEAT_S:
                self._store.touch(live.id, live.end)
                self._flushed[game.name] = now

    def _close(self, name: str, now: float) -> None:
        live = self._live.pop(name)
        live.end = max(live.end, now)
        self._store.touch(live.id, live.end)

    def flush(self) -> None:
        now = time.time()
        for live in self._live.values():
            live.end = max(live.end, now)
            self._store.touch(live.id, live.end)

    # --- Abfragen für die Anzeige -------------------------------------------

    def running(self) -> list[str]:
        """Laufende Spiele in Konfigurationsreihenfolge."""
        return [g.name for g in self._games if g.name in self._live]

    def live_channel(self, game: str) -> Optional[str]:
        live = self._live.get(game)
        return live.channel if live else None

    def channels(self, game: str) -> list[str]:
        return sort_channels(r.channel for r in self._rows if r.game == game and r.channel)

    def _match(self, game: str, channel: str) -> list[SessionRow]:
        return [r for r in self._rows if r.game == game and (not channel or r.channel == channel)]

    def sessions(self, game: str, channel: str = "") -> list[tuple[float, float]]:
        return [(r.start, r.end) for r in self._match(game, channel)]

    def current_duration(self, game: str, channel: str = "") -> float:
        """Laufende Session, sonst Dauer der letzten (für die Offline-Anzeige)."""
        live = self._live.get(game)
        if live is not None and (not channel or live.channel == channel):
            return max(0.0, time.time() - live.start)
        rows = self._match(game, channel)
        return rows[-1].end - rows[-1].start if rows else 0.0
