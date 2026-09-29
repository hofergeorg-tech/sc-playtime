"""Baut dist/SC-Playtime.exe (PyInstaller, eine Datei, ohne Konsole).

    .venv\\Scripts\\python.exe build.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"

# Qt-Module, die das Overlay nicht braucht — spart deutlich Größe.
EXCLUDES = [
    "PySide6.QtNetwork", "PySide6.QtQml", "PySide6.QtQuick", "PySide6.QtQuickWidgets",
    "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.QtWebChannel",
    "PySide6.QtMultimedia", "PySide6.QtPdf", "PySide6.QtSql", "PySide6.QtSvg",
    "PySide6.Qt3DCore", "PySide6.QtCharts", "PySide6.QtDataVisualization",
    "PySide6.QtOpenGL", "PySide6.QtOpenGLWidgets", "tkinter", "unittest",
]
DOCS = ["HILFE.md", "CHANGELOG.md"]


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
    icon = BUILD / "sc-playtime.ico"
    make_icon(icon)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--onefile", "--windowed",
        "--name", "SC-Playtime",
        "--icon", str(icon),
        "--distpath", str(ROOT / "dist"),
        "--workpath", str(BUILD / "pyinstaller"),
        "--specpath", str(BUILD),
        "--paths", str(ROOT),
    ]
    for mod in EXCLUDES:
        cmd += ["--exclude-module", mod]
    for doc in DOCS:  # für Menü → Hilfe / Was ist neu?
        cmd += ["--add-data", f"{ROOT / doc}{os.pathsep}."]
    cmd.append(str(ROOT / "run.pyw"))
    subprocess.run(cmd, check=True)
    print(f"\nFertig: {ROOT / 'dist' / 'SC-Playtime.exe'}")


if __name__ == "__main__":
    main()
