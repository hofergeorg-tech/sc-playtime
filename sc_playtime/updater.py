"""Update-Prüfung über GitHub Releases und Selbst-Update der EXE.

Nur ``urllib`` (kein QtNetwork, das der Build ausschließt). Die Prüfung liest
ausschließlich die öffentliche Release-Info; es werden keine Nutzerdaten gesendet.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from . import __version__

REPO = "hofergeorg-tech/sc-playtime"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"
RELEASES_URL = f"https://github.com/{REPO}/releases/latest"
ASSET_NAME = "SC-Playtime.exe"
TIMEOUT_S = 15


@dataclass(frozen=True)
class Release:
    version: str
    notes: str
    page_url: str
    exe_url: Optional[str]


def parse_version(text: str) -> tuple[int, ...]:
    """``"v1.2.0"`` → ``(1, 2, 0)``; Unlesbares → ``(0,)``."""
    try:
        return tuple(int(p) for p in text.strip().lstrip("vV").split("."))
    except ValueError:
        return (0,)


def is_newer(latest: str, current: str = __version__) -> bool:
    return parse_version(latest) > parse_version(current)


def is_frozen() -> bool:
    """Läuft als PyInstaller-EXE (nur dann ist Selbst-Update möglich)."""
    return bool(getattr(sys, "frozen", False))


def _request(url: str, accept: str) -> urllib.request.Request:
    return urllib.request.Request(url, headers={"User-Agent": f"SC-Playtime/{__version__}", "Accept": accept})


def fetch_latest() -> Release:
    with urllib.request.urlopen(_request(API_URL, "application/vnd.github+json"), timeout=TIMEOUT_S) as resp:
        data = json.load(resp)
    exe_url = next(
        (a["browser_download_url"] for a in data.get("assets", []) if a.get("name") == ASSET_NAME), None
    )
    return Release(
        version=str(data.get("tag_name", "")).lstrip("vV"),
        notes=data.get("body") or "",
        page_url=data.get("html_url") or RELEASES_URL,
        exe_url=exe_url,
    )


def download(url: str) -> Path:
    """Lädt die neue EXE in einen Temp-Ordner und gibt den Pfad zurück."""
    dest = Path(tempfile.mkdtemp(prefix="sc-playtime-update-")) / ASSET_NAME
    with urllib.request.urlopen(_request(url, "application/octet-stream"), timeout=120) as resp, \
            dest.open("wb") as out:
        while chunk := resp.read(1 << 16):
            out.write(chunk)
    if dest.stat().st_size < 1_000_000:  # eine echte Build-EXE ist deutlich größer
        raise OSError("Download unvollständig")
    return dest


def install_script(new_exe: Path, target: Path, restart: bool = True) -> str:
    """Batch, die wartet bis ``target`` frei ist, es ersetzt und neu startet.

    ``ping`` statt ``timeout`` als Pause, weil ``timeout`` ohne Konsole abbricht.
    Nach 60 Versuchen (~1 min) wird aufgegeben, damit nichts ewig hängt.
    """
    lines = [
        "@echo off",
        "set n=0",
        ":retry",
        f'move /Y "{new_exe}" "{target}" >nul 2>&1 && goto done',
        "set /a n+=1",
        "if %n% geq 60 goto end",
        "ping -n 2 127.0.0.1 >nul",
        "goto retry",
        ":done",
    ]
    if restart:
        lines.append(f'start "" "{target}"')
    lines += [":end", f'rmdir /S /Q "{new_exe.parent}" >nul 2>&1', '(goto) 2>nul & del "%~f0"']
    return "\r\n".join(lines) + "\r\n"


def start_install(new_exe: Path, target: Optional[Path] = None, restart: bool = True) -> None:
    """Startet den Austausch im Hintergrund. Danach muss sich die App beenden."""
    target = target or Path(sys.executable)
    bat = Path(tempfile.gettempdir()) / "sc-playtime-update.bat"
    bat.write_text(install_script(new_exe, target, restart), encoding="ascii", errors="replace")
    env = dict(os.environ)
    # neue EXE soll ihren eigenen Temp-Ordner entpacken, nicht den der alten erben
    env["PYINSTALLER_RESET_ENVIRONMENT"] = "1"
    flags = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    subprocess.Popen(["cmd.exe", "/c", str(bat)], creationflags=flags, env=env, close_fds=True)
