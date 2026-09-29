"""Baut eine einzelne Programmdatei ohne Konsole (PyInstaller).

    Windows:  .venv\\Scripts\\python.exe build.py   → dist/SC-Playtime.exe
    Linux:    .venv/bin/python build.py            → dist/SC-Playtime

Der GitHub-Workflow (.github/workflows/ci.yml) baut beide bei jedem Versions-Tag.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"

# Qt-Module, die das Overlay nicht braucht — spart deutlich Größe.
# QtSvg bleibt drin: die Flaggen im Sprachmenü sind SVGs.
EXCLUDES = [
    "PySide6.QtNetwork", "PySide6.QtQml", "PySide6.QtQuick", "PySide6.QtQuickWidgets",
    "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.QtWebChannel",
    "PySide6.QtMultimedia", "PySide6.QtPdf", "PySide6.QtSql",
    "PySide6.Qt3DCore", "PySide6.QtCharts", "PySide6.QtDataVisualization",
    "PySide6.QtOpenGL", "PySide6.QtOpenGLWidgets", "tkinter", "unittest",
]
# Hilfe/Changelog je Sprache (Menü → Hilfe / Was ist neu?)
DOCS = ["HILFE.md", "HELP.md", "CHANGELOG.md", "CHANGELOG.en.md"]


def make_icon(path: Path) -> None:
    """Das zur Laufzeit gezeichnete App-Icon als .ico für die EXE speichern."""
    from PySide6 import QtWidgets

    sys.path.insert(0, str(ROOT))
    from sc_playtime.ui import app_icon

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    pixmap = app_icon().pixmap(64, 64)
    if not pixmap.save(str(path), "ICO"):
        raise SystemExit(f"Icon konnte nicht geschrieben werden: {path}")


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--onefile", "--windowed",
        "--name", "SC-Playtime",
        "--distpath", str(ROOT / "dist"),
        "--workpath", str(BUILD / "pyinstaller"),
        "--specpath", str(BUILD),
        "--paths", str(ROOT),
        "--hidden-import", "PySide6.QtSvg",  # lädt das SVG-Bildformat-Plugin
    ]
    if sys.platform == "win32":  # Linux-Programme haben kein eingebettetes Icon
        icon = BUILD / "sc-playtime.ico"
        make_icon(icon)
        cmd += ["--icon", str(icon)]
    for mod in EXCLUDES:
        cmd += ["--exclude-module", mod]
    for doc in DOCS:
        cmd += ["--add-data", f"{ROOT / doc}{os.pathsep}."]
    cmd += ["--add-data", f"{ROOT / 'assets'}{os.pathsep}assets"]
    cmd.append(str(ROOT / "run.pyw"))
    subprocess.run(cmd, check=True)
    name = "SC-Playtime.exe" if sys.platform == "win32" else "SC-Playtime"
    print(f"\nFertig: {ROOT / 'dist' / name}")


if __name__ == "__main__":
    main()
