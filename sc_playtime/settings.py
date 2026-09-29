"""Einstellungen und Datenordner (%APPDATA%\\SC-Playtime)."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Optional

from .tracker import Game

DEFAULT_GAMES = [{"name": "Star Citizen", "exe": "StarCitizen.exe"}]


def data_dir() -> Path:
    """Windows: %APPDATA%\\SC-Playtime, Linux: $XDG_DATA_HOME/SC-Playtime (~/.local/share)."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or Path.home())
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    path = base / "SC-Playtime"
    path.mkdir(parents=True, exist_ok=True)
    return path


@dataclass
class Settings:
    x: Optional[int] = None
    y: Optional[int] = None
    expanded: bool = False
    tab: str = "day"
    games: list[dict] = field(default_factory=lambda: [dict(g) for g in DEFAULT_GAMES])
    game: str = "Star Citizen"  # angezeigtes Spiel, solange keins läuft
    channel: str = ""  # Filter, "" = alle Channels
    bg_alpha: int = 80  # Hintergrund-Deckkraft in %
    opacity: int = 100  # Gesamt-Deckkraft in %
    chip_bg: str = ""  # aktiver Channel-Chip: Hintergrund (#rrggbb), "" = Channel-Farbe
    chip_fg: str = ""  # aktiver Channel-Chip: Schrift (#rrggbb), "" = dunkel
    tile_bg: str = "#64ffb4"  # Statistik-Kacheln im Spiel: Hintergrund, "" = nicht einfärben
    tile_fg: str = "#04141a"  # Statistik-Kacheln im Spiel: Schrift, "" = hell
    language: str = ""  # "de", "en", … ; "" = Sprache des Systems
    auto_update: bool = True  # beim Start und alle 12 h nach Updates suchen
    seen_version: str = ""  # zuletzt gestartete Version → "Was ist neu?" nach Update
    locked: bool = False
    click_through: bool = False
    hide_when_offline: bool = False

    @classmethod
    def load(cls, path: Path) -> "Settings":
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return cls()
        known = {f.name for f in fields(cls)}
        s = cls(**{k: v for k, v in raw.items() if k in known})
        if not s.games:
            s.games = [dict(g) for g in DEFAULT_GAMES]
        return s

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2, ensure_ascii=False), encoding="utf-8")

    def game_list(self) -> list[Game]:
        return [Game(g["name"], g["exe"]) for g in self.games if g.get("name") and g.get("exe")]
