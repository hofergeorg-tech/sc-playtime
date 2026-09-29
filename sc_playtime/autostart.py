"""Autostart über HKCU\\...\\Run (kein Admin nötig)."""

from __future__ import annotations

import sys
import winreg
from pathlib import Path

_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
_NAME = "SC-Playtime"


def command() -> str:
    if getattr(sys, "frozen", False):  # PyInstaller-Build
        return f'"{sys.executable}"'
    exe = Path(sys.executable)
    windowless = exe.with_name("pythonw.exe")  # kein Konsolenfenster beim Login
    if windowless.exists():
        exe = windowless
    script = Path(__file__).resolve().parent.parent / "run.pyw"
    return f'"{exe}" "{script}"'


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
            winreg.SetValueEx(key, _NAME, 0, winreg.REG_SZ, command())
        else:
            try:
                winreg.DeleteValue(key, _NAME)
            except FileNotFoundError:
                pass
