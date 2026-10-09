"""Verfolgt die konfigurierten Spiele (EXE-Namen) und schreibt daraus Sessions.

AFK-Erkennung (optional): Gibt es länger als ``afk_s`` keine Eingabe am PC,
endet die Session beim letzten Tastendruck. Sobald wieder eine Eingabe kommt
und das Spiel noch läuft, beginnt eine neue Session.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional

from . import endings, process
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
        game_dir: Callable[[Optional[str]], Optional[Path]] = endings.channel_dir,
        ending: Callable[[Path, float], str] = endings.reason_for_dir,
        on_dir: Optional[Callable[[Path], None]] = None,
    ) -> None:
        self._store = store
        self._find = find
        self._start_time = start_time
        self._image_path = image_path
        self._version = version
        self._idle = idle
        self._game_dir = game_dir
        self._ending = ending
        self._on_dir = on_dir  # meldet Installationsordner (für die Nachträge beim Start)
        self._dirs: dict[str, Path] = {}  # game name → Channel-Ordner des laufenden Spiels
        self.afk_s = afk_s  # 0 = AFK-Erkennung aus
        self._games: list[Game] = list(games)
        self._rows: list[SessionRow] = store.all()
        self._live: dict[str, SessionRow] = {}  # game name → laufende Session
        self._paused: dict[str, SessionRow] = {}  # game name → letzte Session vor der AFK-Pause
        self._flushed: dict[str, float] = {}
        # Steigt, sobald sich abgeschlossene Sessions ändern (nicht beim bloßen
        # Verlängern der laufenden) → die Anzeige kann ihre Auswertung zwischenspeichern.
        self.revision = 0

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
                paused = self._paused.pop(game.name, None)
                last = self._live.get(game.name) or (paused if paused is not None and paused.id else None)
                if game.name in self._live:
                    self._close(game.name, now)
                if last is not None:
                    self._finish(game.name, last)
                self._dirs.pop(game.name, None)
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
        if channel is None or name not in self._dirs:
            image = self._image_path(pid)
            if channel is None:
                channel = process.channel_from_path(image)
            folder = self._game_dir(image)
            if folder is not None:
                self._dirs[name] = folder
                if self._on_dir is not None:
                    self._on_dir(folder)
        if version is None:
            version = self._version(pid)
        row = self._store.open(name, channel, start, now, version)
        live = next((r for r in self._rows if r.id == row.id), None)
        if live is None:
            live = row
            self._rows.append(live)
        self._live[name] = live
        self._flushed[name] = now
        self.revision += 1
        return live

    def _close(self, name: str, end: float, extend: bool = True) -> None:
        live = self._live.pop(name)
        live.end = max(live.end, end) if extend else end
        self._store.touch(live.id, live.end)
        self.revision += 1

    def _finish(self, name: str, last: SessionRow) -> None:
        """Das Spiel ist beendet: wie endete es? (nur Spiele mit bekanntem Log, z. B. Star Citizen)"""
        folder = self._dirs.get(name)
        if folder is None:
            return
        reason = self._ending(folder, last.start)
        if reason:
            last.reason = reason
            self._store.set_reason(last.id, reason)
            self.revision += 1

    def set_reasons(self, updates: Iterable[tuple[int, str]]) -> None:
        """Nachträglich ermittelte Ende-Angaben übernehmen (aus den gesicherten Logs)."""
        by_id = {r.id: r for r in self._rows}
        changed = False
        for sid, reason in updates:
            row = by_id.get(sid)
            if row is not None and not row.reason:
                row.reason = reason
                self._store.set_reason(sid, reason)
                changed = True
        if changed:
            self.revision += 1

    def reload(self) -> None:
        """Nach dem Zusammenführen: Sessions neu aus der DB lesen (laufende bleiben verknüpft)."""
        live_ids = {r.id: name for name, r in self._live.items()}
        self._rows = self._store.all()
        for r in self._rows:
            if r.id in live_ids:
                self._live[live_ids[r.id]] = r
        self.revision += 1

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
        self.revision += 1

    def delete_session(self, session_id: int) -> None:
        if self.is_live(session_id):
            raise ValueError("laufende Session")
        self._store.delete(session_id)
        self._rows = [r for r in self._rows if r.id != session_id]
        self.revision += 1

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
        return [SessionRow(r.id, r.game, r.channel, r.start, r.end, r.version, r.reason)
                for r in self._rows if game is None or r.game == game]

    def _match(self, game: str, channel: str) -> list[SessionRow]:
        return [r for r in self._rows if r.game == game and (not channel or r.channel == channel)]

    def sessions(self, game: str, channel: str = "") -> list[tuple[float, float]]:
        return [(r.start, r.end) for r in self._match(game, channel)]

    def _live_row(self, game: str, channel: str) -> Optional[SessionRow]:
        live = self._live.get(game)
        return None if live is None or (channel and live.channel != channel) else live

    def closed_sessions(self, game: str, channel: str = "") -> list[tuple[float, float]]:
        """Alle Sessions außer der laufenden – ändern sich nur zusammen mit :attr:`revision`."""
        live = self._live_row(game, channel)
        return [(r.start, r.end) for r in self._match(game, channel) if r is not live]

    def live_span(self, game: str, channel: str = "") -> Optional[tuple[float, float]]:
        """Start und bisheriges Ende der laufenden Session (wächst jede Sekunde)."""
        live = self._live_row(game, channel)
        return (live.start, live.end) if live is not None else None

    def versioned(self, game: str, channel: str = "") -> list[tuple[str, float, float, str]]:
        """(Patch, Start, Ende, wie beendet) je Session."""
        return [(r.version, r.start, r.end, r.reason) for r in self._match(game, channel)]

    def current_duration(self, game: str, channel: str = "") -> float:
        """Laufende Session, sonst Dauer der letzten (für die Offline-Anzeige)."""
        live = self._live.get(game)
        if live is not None and (not channel or live.channel == channel):
            return max(0.0, time.time() - live.start)
        rows = self._match(game, channel)
        return rows[-1].end - rows[-1].start if rows else 0.0
