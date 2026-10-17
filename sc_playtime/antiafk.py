"""Anti-AFK: hält das Spiel wach (nur Windows).

Zwei unabhängige Aktionen mit eigenem Takt in Sekunden: die Maus ein Muster
abfahren lassen (rechts–links, hoch–runter, Quadrat, Kreis, zufällig; Weite in
Pixeln, am Ende steht sie wieder am Ausgangspunkt) und die Taste rechts neben P
drücken (deutsch Ü, englisch [). Solange Anti-AFK eingeschaltet ist, laufen
beide im Takt – auch während man selbst spielt –, aber nur, wenn ein
überwachtes Spiel im Vordergrund ist; man tippt also nie versehentlich in einen
Chat. Gesendet
werden physische Tasten (Scancodes): Star Citizen ignoriert reine Tastencodes,
wie sie z. B. Move Mouse schickt.

Die eigenen Eingaben zählen nicht als Aktivität: ``idle_seconds`` liefert die
Zeit seit der letzten *echten* Eingabe, damit die AFK-Erkennung weiter greift.
"""

from __future__ import annotations

import math
import random
import sys
import threading
import time
from pathlib import Path
from typing import Callable, Iterable, Optional

from . import process

SUPPORTED = sys.platform == "win32"
SCANCODE = 0x1A  # Taste rechts neben P: Ü (DE), [ (US), ^ (FR) …
PATTERNS = ("horizontal", "vertical", "square", "circle", "random")
MOUSE_INTERVALS = (5, 10, 30, 60, 120, 300)  # Sekunden im Menü
KEY_INTERVALS = (5, 10, 30, 60, 120)
MAX_PIXELS = 100
POLL_MS = 500
PRESS_S = 0.06  # so lange bleibt die Taste gedrückt, damit das Spiel sie sicher sieht
SPEEDS = {"slow": 60, "medium": 150, "fast": 400}  # Pixel pro Sekunde
FRAME_S = 0.008  # Maus gleitet in ~125 kleinen Schritten pro Sekunde


def mouse_path(pattern: str, pixels: int, rng: Callable[[], float] = random.random) -> list[tuple[int, int]]:
    """Relative Mausschritte für ein Muster; ihre Summe ist immer (0, 0)."""
    d = max(1, min(MAX_PIXELS, int(pixels)))
    if pattern == "vertical":
        return [(0, d), (0, -d)]
    if pattern == "square":
        return [(d, 0), (0, d), (-d, 0), (0, -d)]
    if pattern in ("circle", "random"):
        if pattern == "random":
            a = rng() * 2 * math.pi
            x, y = round(d * math.cos(a)), round(d * math.sin(a))
            if (x, y) == (0, 0):
                x = d
            return [(x, y), (-x, -y)]
        n = max(8, min(32, d))  # kleiner Kreis: wenige Schritte, großer: runder
        pts = [(round(d * math.cos(2 * math.pi * i / n)) - d, round(d * math.sin(2 * math.pi * i / n)))
               for i in range(n + 1)]
        return [(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]) if a != b]
    return [(d, 0), (-d, 0)]


def unit_steps(steps: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Zerlegt Mausschritte in Einzelpixel, damit die Bewegung gleitet statt springt."""
    out = []
    for dx, dy in steps:
        n = max(abs(dx), abs(dy))
        px = py = 0
        for i in range(1, n + 1):
            x, y = round(dx * i / n), round(dy * i / n)
            out.append((x - px, y - py))
            px, py = x, y
    return out


class AntiAfk:
    def __init__(
        self,
        settings,
        exe_names: Callable[[], Iterable[str]],
        last_input: Optional[Callable[[], Optional[int]]] = None,
        tick: Optional[Callable[[], int]] = None,
        foreground_exe: Optional[Callable[[], Optional[str]]] = None,
        send_key: Optional[Callable[[], None]] = None,
        move_mouse: Optional[Callable[[list[tuple[int, int]], int], None]] = None,
        run_async: Optional[Callable[[Callable[[], None]], None]] = None,
    ) -> None:
        self._s = settings
        self._exe_names = exe_names
        self._last_input = last_input or _last_input
        self._tick = tick or _tick
        self._foreground_exe = foreground_exe or _foreground_exe
        self._send_key = send_key or _send_key
        self._move_mouse = move_mouse or _move_mouse
        # Mausbewegung im Hintergrund, damit die Anzeige währenddessen nicht hängt
        self._run_async = run_async or (lambda fn: threading.Thread(target=fn, daemon=True).start())
        self._moving = False
        self._injected: Optional[int] = None  # GetLastInputInfo direkt nach unserer letzten Eingabe
        self._real: Optional[int] = None  # letzte echte Eingabe
        self._last: dict[str, int] = {}  # Aktion → Zeitpunkt (ms) des letzten Sendens
        self.waiting = False  # zuletzt fällig, aber das Spiel war nicht im Vordergrund

    @property
    def active(self) -> bool:
        return bool(self._s.anti_afk_on and (self._s.anti_afk_mouse or self._s.anti_afk_key))

    def _real_input(self) -> Optional[int]:
        cur = self._last_input()
        if cur is None:
            return None
        if self._moving:  # eigene Mausbewegung läuft gerade
            if self._real is None:
                self._real = cur
        elif cur != self._injected:
            self._real = cur
        return self._real

    def idle_seconds(self) -> Optional[float]:
        """Sekunden seit der letzten echten Eingabe (ohne die von Anti-AFK)."""
        if not SUPPORTED and self._last_input is _last_input:
            return process.idle_seconds()
        real = self._real_input()
        if real is None:
            return None
        return ((self._tick() - real) & 0xFFFFFFFF) / 1000.0

    def progress(self) -> list[tuple[str, float]]:
        """Eingeschaltete Aktionen mit Anteil (0–1) der Zeit bis zum nächsten Senden, für die Anzeige."""
        if not self.active:
            return []
        now = self._tick()
        out = []
        for action, on, every in (("key", self._s.anti_afk_key, self._s.anti_afk_key_s),
                                  ("mouse", self._s.anti_afk_mouse, self._s.anti_afk_mouse_s)):
            if on:
                last = self._last.get(action)
                done = 1.0 if last is None else ((now - last) & 0xFFFFFFFF) / 1000.0 / max(1, int(every))
                out.append((action, min(1.0, done)))
        return out

    def _due(self, action: str, every_s: int, now: int) -> bool:
        every = max(1, int(every_s))
        last = self._last.get(action)
        return last is None or ((now - last) & 0xFFFFFFFF) / 1000.0 >= every

    def poll(self) -> list[str]:
        """Alle ``POLL_MS`` aufrufen. Liefert die gesendeten Aktionen ("mouse", "key")."""
        if not self.active:
            return []
        self.idle_seconds()  # letzte echte Eingabe merken, bevor eigene sie überdecken
        now = self._tick()
        due = [a for a, on, every in (("mouse", self._s.anti_afk_mouse, self._s.anti_afk_mouse_s),
                                      ("key", self._s.anti_afk_key, self._s.anti_afk_key_s))
               if on and self._due(a, every, now)]
        if not due:
            return []
        exe = self._foreground_exe()
        self.waiting = not exe or exe.lower() not in {n.lower() for n in self._exe_names()}
        if self.waiting:
            return []
        sent = []
        for action in due:
            if action == "mouse":
                if self._moving:
                    continue  # vorige Bewegung noch nicht fertig
                self._moving = True
                path = mouse_path(self._s.anti_afk_pattern, self._s.anti_afk_pixels)
                speed = SPEEDS.get(self._s.anti_afk_speed, SPEEDS["medium"])

                def glide(path=path, speed=speed) -> None:
                    try:
                        self._move_mouse(path, speed)
                    finally:
                        self._injected = self._last_input()
                        self._moving = False

                self._run_async(glide)
            else:
                self._send_key()
                self._injected = self._last_input()
            self._last[action] = now
            sent.append(action)
        return sent


def key_name() -> str:
    """Name der Taste im aktuellen Tastaturlayout (Ü, [, ^ …)."""
    if SUPPORTED:
        import ctypes

        buf = ctypes.create_unicode_buffer(32)
        if ctypes.windll.user32.GetKeyNameTextW(SCANCODE << 16, buf, len(buf)):
            return buf.value.upper()
    return "Ü"


# --- Windows (Win32 über ctypes) ---------------------------------------------

if SUPPORTED:
    import ctypes
    from ctypes import wintypes

    _user32 = ctypes.WinDLL("user32")
    _kernel32 = ctypes.WinDLL("kernel32")

    _INPUT_MOUSE, _INPUT_KEYBOARD = 0, 1
    _MOUSEEVENTF_MOVE = 0x0001
    _KEYEVENTF_KEYUP, _KEYEVENTF_SCANCODE = 0x0002, 0x0008

    class _MOUSEINPUT(ctypes.Structure):
        _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG), ("mouseData", wintypes.DWORD),
                    ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.c_size_t)]

    class _KEYBDINPUT(ctypes.Structure):
        _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD), ("dwFlags", wintypes.DWORD),
                    ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.c_size_t)]

    class _HARDWAREINPUT(ctypes.Structure):
        _fields_ = [("uMsg", wintypes.DWORD), ("wParamL", wintypes.WORD), ("wParamH", wintypes.WORD)]

    class _INPUTUNION(ctypes.Union):
        _fields_ = [("mi", _MOUSEINPUT), ("ki", _KEYBDINPUT), ("hi", _HARDWAREINPUT)]

    class _INPUT(ctypes.Structure):
        _fields_ = [("type", wintypes.DWORD), ("u", _INPUTUNION)]

    _user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(_INPUT), ctypes.c_int]
    _user32.SendInput.restype = wintypes.UINT
    _user32.GetForegroundWindow.restype = wintypes.HWND
    _user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    _user32.GetWindowThreadProcessId.restype = wintypes.DWORD

    class _LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]

    _user32.GetLastInputInfo.argtypes = [ctypes.POINTER(_LASTINPUTINFO)]
    _user32.GetLastInputInfo.restype = wintypes.BOOL
    _kernel32.GetTickCount.restype = wintypes.DWORD

    def _send(*inputs: _INPUT) -> None:
        arr = (_INPUT * len(inputs))(*inputs)
        _user32.SendInput(len(inputs), arr, ctypes.sizeof(_INPUT))

    def _key(flags: int) -> _INPUT:
        return _INPUT(_INPUT_KEYBOARD, _INPUTUNION(ki=_KEYBDINPUT(0, SCANCODE, _KEYEVENTF_SCANCODE | flags, 0, 0)))

    def _mouse(dx: int, dy: int) -> _INPUT:
        return _INPUT(_INPUT_MOUSE, _INPUTUNION(mi=_MOUSEINPUT(dx, dy, 0, _MOUSEEVENTF_MOVE, 0, 0)))

    def _send_key() -> None:
        _send(_key(0))
        time.sleep(PRESS_S)
        _send(_key(_KEYEVENTF_KEYUP))

    def _move_mouse(steps: list[tuple[int, int]], speed: int) -> None:
        """Fährt den Weg gleichmäßig mit ``speed`` Pixeln pro Sekunde ab."""
        units = unit_steps(steps)
        start, done = time.perf_counter(), 0
        while done < len(units):
            time.sleep(FRAME_S)
            target = min(len(units), int((time.perf_counter() - start) * speed) + 1)
            dx = sum(u[0] for u in units[done:target])
            dy = sum(u[1] for u in units[done:target])
            if dx or dy:
                _send(_mouse(dx, dy))
            done = target

    def _last_input() -> Optional[int]:
        info = _LASTINPUTINFO()
        info.cbSize = ctypes.sizeof(_LASTINPUTINFO)
        return int(info.dwTime) if _user32.GetLastInputInfo(ctypes.byref(info)) else None

    def _tick() -> int:
        return int(_kernel32.GetTickCount())

    def _foreground_exe() -> Optional[str]:
        hwnd = _user32.GetForegroundWindow()
        if not hwnd:
            return None
        pid = wintypes.DWORD()
        _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        image = process.process_image_path(int(pid.value)) if pid.value else None
        return Path(image).name if image else None
else:
    def _send_key() -> None:
        pass

    def _move_mouse(steps: list[tuple[int, int]], speed: int) -> None:
        pass

    def _last_input() -> Optional[int]:
        return None

    def _tick() -> int:
        return int(time.monotonic() * 1000) & 0xFFFFFFFF

    def _foreground_exe() -> Optional[str]:
        return None
