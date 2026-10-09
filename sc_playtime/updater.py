"""Update-Prüfung über GitHub Releases und Selbst-Update der EXE.

Nur ``urllib`` (kein QtNetwork, das der Build ausschließt). Die Prüfung liest
ausschließlich die öffentliche Release-Info; es werden keine Nutzerdaten gesendet.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
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
# Name der Datei im Release je Plattform (so lädt der CI-Build sie hoch)
ASSET_NAME = "SC-Playtime.exe" if sys.platform == "win32" else "SC-Playtime-linux-x86_64"
TIMEOUT_S = 15


@dataclass(frozen=True)
class Release:
    version: str
    notes: str
    page_url: str
    exe_url: Optional[str]
    # SHA-256 der Datei, wie GitHub sie beim Hochladen berechnet hat (hex); None bei alten Releases
    sha256: Optional[str] = None


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
        return parse_release(json.load(resp))


def parse_release(data: dict) -> Release:
    asset = next((a for a in data.get("assets", []) if a.get("name") == ASSET_NAME), None)
    digest = str((asset or {}).get("digest") or "")
    return Release(
        version=str(data.get("tag_name", "")).lstrip("vV"),
        notes=data.get("body") or "",
        page_url=data.get("html_url") or RELEASES_URL,
        exe_url=asset["browser_download_url"] if asset else None,
        sha256=digest[len("sha256:"):].lower() if digest.lower().startswith("sha256:") else None,
    )


def matches_checksum(path: Path, sha256: Optional[str]) -> bool:
    """Ist die Datei genau die, die GitHub für das Release hat? (ohne Prüfsumme: ja)"""
    if not sha256:
        return True
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest() == sha256.lower()


def download(url: str, sha256: Optional[str] = None) -> Path:
    """Lädt die neue EXE in einen Temp-Ordner und gibt den Pfad zurück."""
    dest = Path(tempfile.mkdtemp(prefix="sc-playtime-update-")) / ASSET_NAME
    with urllib.request.urlopen(_request(url, "application/octet-stream"), timeout=120) as resp, \
            dest.open("wb") as out:
        while chunk := resp.read(1 << 16):
            out.write(chunk)
    if dest.stat().st_size < 1_000_000:  # eine echte Build-EXE ist deutlich größer
        shutil.rmtree(dest.parent, ignore_errors=True)
        raise OSError("Download unvollständig")
    if not matches_checksum(dest, sha256):
        shutil.rmtree(dest.parent, ignore_errors=True)
        raise OSError("Download passt nicht zur Prüfsumme des Releases")
    return dest


def install_script(new_exe: Path, target: Path, restart: bool = True) -> str:
    """Windows-Batch, die wartet bis ``target`` frei ist, es ersetzt und neu startet.

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
    """Tauscht die Programmdatei aus und startet neu. Danach muss sich die App beenden."""
    target = target or Path(sys.executable)
    env = dict(os.environ)
    # neue EXE soll ihren eigenen Temp-Ordner entpacken, nicht den der alten erben
    env["PYINSTALLER_RESET_ENVIRONMENT"] = "1"
    if sys.platform == "win32":
        # Windows sperrt die laufende EXE → Austausch per Batch, sobald sie beendet ist
        bat = Path(tempfile.gettempdir()) / "sc-playtime-update.bat"
        bat.write_text(install_script(new_exe, target, restart), encoding="ascii", errors="replace")
        flags = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        subprocess.Popen(["cmd.exe", "/c", str(bat)], creationflags=flags, env=env, close_fds=True)
        return
    # Linux: laufende Datei darf ersetzt werden. Erst neben das Ziel kopieren
    # (Temp kann ein anderes Dateisystem sein), dann atomar umbenennen.
    staged = target.with_name(f".{target.name}.new")
    shutil.copyfile(new_exe, staged)
    staged.chmod(0o755)
    os.replace(staged, target)
    shutil.rmtree(new_exe.parent, ignore_errors=True)
    if restart:
        # kurz warten, bis die alte Instanz ihre Sperrdatei freigegeben hat
        subprocess.Popen(["sh", "-c", 'sleep 2; exec "$0"', str(target)], env=env, start_new_session=True)
