"""Globale Tastenkürzel, die auch im Spiel funktionieren (nur Windows).

Windows: ``RegisterHotKey`` in einem eigenen Thread mit Nachrichtenschleife;
der Rückruf läuft in diesem Thread (die Oberfläche reicht ihn per Qt-Signal
weiter). Unter Linux gibt es keine portable Lösung (Wayland verbietet globale
Tastenkürzel) — dort meldet ``set`` jedes Kürzel als nicht registriert.
"""

from __future__ import annotations

import sys
import threading
from typing import Callable, Optional

MOD_ALT, MOD_CONTROL, MOD_SHIFT, MOD_WIN, MOD_NOREPEAT = 0x1, 0x2, 0x4, 0x8, 0x4000
_MODS = {"ctrl": MOD_CONTROL, "shift": MOD_SHIFT, "alt": MOD_ALT, "meta": MOD_WIN}
_NAMED = {
    "home": 0x24, "end": 0x23, "ins": 0x2D, "del": 0x2E, "pgup": 0x21, "pgdown": 0x22,
    "pause": 0x13, "scrolllock": 0x91, "space": 0x20,
    "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28,
}

SUPPORTED = sys.platform == "win32"


def parse(text: str) -> Optional[tuple[int, int]]:
    """``"Ctrl+Shift+F9"`` (Qt-PortableText) → (Modifier-Bits, virtueller Tastencode).

    Nur mit mindestens einer Zusatztaste (außer F-Tasten), damit normales
    Tippen nicht abgefangen wird.
    """
    parts = [p.strip().lower() for p in text.replace(" ", "").split("+")]
    if not parts or not parts[-1]:
        return None
    *mods, key = parts
    bits = 0
    for m in mods:
        if m not in _MODS:
            return None
        bits |= _MODS[m]
    if len(key) == 1 and (key.isascii() and key.isalnum()):
        vk = ord(key.upper())
    elif key.startswith("f") and key[1:].isdigit() and 1 <= int(key[1:]) <= 24:
        vk = 0x70 + int(key[1:]) - 1
    elif key in _NAMED:
        vk = _NAMED[key]
    else:
        return None
    if bits == 0 and not 0x70 <= vk <= 0x87:
        return None
    return bits, vk


class Hotkeys:
    def __init__(self, on_hotkey: Callable[[int], None]) -> None:
        self._on_hotkey = on_hotkey
        self._thread: Optional[threading.Thread] = None
        self._thread_id = 0

    def set(self, bindings: dict[int, str]) -> dict[int, bool]:
        """Ersetzt alle Kürzel (id → Text, leer = keins). Liefert id → erfolgreich."""
        self.stop()
        wanted = {i: parse(t) for i, t in bindings.items() if t}
        result = {i: False for i in bindings}
        if not SUPPORTED or not any(wanted.values()):
            return result
        ready = threading.Event()
        self._thread = threading.Thread(target=self._run, args=(wanted, result, ready), daemon=True)
        self._thread.start()
        ready.wait(2.0)
        return result

    def stop(self) -> None:
        if self._thread is None:
            return
        import ctypes

        wm_quit = 0x0012
        ctypes.windll.user32.PostThreadMessageW(self._thread_id, wm_quit, 0, 0)
        self._thread.join(2.0)
        self._thread = None

    def _run(self, wanted: dict[int, Optional[tuple[int, int]]], result: dict[int, bool],
             ready: threading.Event) -> None:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        self._thread_id = ctypes.windll.kernel32.GetCurrentThreadId()
        msg = wintypes.MSG()
        # Nachrichtenschleife anlegen, bevor PostThreadMessage sie erreichen soll
        user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 0)
        for hid, combo in wanted.items():
            if combo is not None:
                result[hid] = bool(user32.RegisterHotKey(None, hid, combo[0] | MOD_NOREPEAT, combo[1]))
        ready.set()
        wm_hotkey = 0x0312
        try:
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
                if msg.message == wm_hotkey:
                    self._on_hotkey(int(msg.wParam))
        finally:
            for hid, ok in result.items():
                if ok:
                    user32.UnregisterHotKey(None, hid)
