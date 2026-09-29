"""Autostart beim Anmelden, ohne Admin-Rechte.

Windows: Eintrag unter HKCU\\...\\Run. Linux: ``~/.config/autostart/*.desktop``
(XDG-Standard, gilt für KDE, GNOME, XFCE, …).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_NAME = "SC-Playtime"


def command() -> list[str]:
    if getattr(sys, "frozen", False):  # PyInstaller-Build
        return [sys.executable]
    exe = Path(sys.executable)
    if sys.platform == "win32":
        windowless = exe.with_name("pythonw.exe")  # kein Konsolenfenster beim Login
        if windowless.exists():
            exe = windowless
    script = Path(__file__).resolve().parent.parent / "run.pyw"
    return [str(exe), str(script)]


if sys.platform == "win32":
    import winreg

    _KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

    def is_enabled() -> bool:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _KEY) as key:
                winreg.QueryValueEx(key, _NAME)
            return True
        except OSError:
            return False

    def set_enabled(enabled: bool) -> None:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _KEY, 0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                winreg.SetValueEx(key, _NAME, 0, winreg.REG_SZ, " ".join(f'"{a}"' for a in command()))
            else:
                try:
                    winreg.DeleteValue(key, _NAME)
                except FileNotFoundError:
                    pass

else:

    def _desktop_file() -> Path:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
        return base / "autostart" / "sc-playtime.desktop"

    def desktop_entry(cmd: list[str]) -> str:
        # Exec-Zeile nach Desktop-Entry-Spec: Argumente in "…", darin \ " ` $ maskieren
        def quote(arg: str) -> str:
            for ch in ("\\", '"', "`", "$"):
                arg = arg.replace(ch, "\\" + ch)
            return f'"{arg}"'

        return (
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Name=SC Playtime\n"
            "Comment=Playtime overlay\n"
            f"Exec={' '.join(quote(a) for a in cmd)}\n"
            "Terminal=false\n"
            "X-GNOME-Autostart-enabled=true\n"
        )

    def is_enabled() -> bool:
        return _desktop_file().exists()

    def set_enabled(enabled: bool) -> None:
        path = _desktop_file()
        if enabled:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(desktop_entry(command()), encoding="utf-8")
        else:
            path.unlink(missing_ok=True)
