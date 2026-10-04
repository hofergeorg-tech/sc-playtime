"""Prozess-Erkennung, nur lesend und ohne Zusatzpakete.

Windows: Prozessliste per Toolhelp-Snapshot, Startzeit per ``GetProcessTimes``.
Linux: ``/proc``. Spiele unter Wine/Proton/Lutris tauchen dort mit ihrem
Windows-Pfad in der Kommandozeile auf (``C:\\...\\StarCitizen.exe``), native
Spiele mit ihrem Programmnamen. Nichts davon greift in das Spiel ein.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path, PureWindowsPath
from typing import Iterable, Optional

_VERSION_RE = re.compile(r"(\d+\.\d+(?:\.\d+)?)")


def version_from_manifest(text: str) -> str:
    """Patch aus ``build_manifest.id``: ``"Branch": "sc-alpha-4.3.1"`` → ``4.3.1``."""
    try:
        data = json.loads(text).get("Data", {})
    except (ValueError, AttributeError):
        return ""
    for key in ("Branch", "Version"):
        m = _VERSION_RE.search(str(data.get(key, "")))
        if m:
            return m.group(1)
    return ""


def version_from_log(lines: Iterable[str]) -> str:
    """Patch aus dem Kopf von ``Game.log`` (Zeile ``Branch: sc-alpha-4.3.1``)."""
    for line in lines:
        if "Branch:" in line:
            m = _VERSION_RE.search(line.split("Branch:", 1)[1])
            if m:
                return m.group(1)
    return ""


def version_in_dirs(dirs: Iterable[Path]) -> str:
    """Erster Patch, der sich in einem der Ordner finden lässt, sonst ``""``."""
    for d in dirs:
        try:
            manifest = d / "build_manifest.id"
            if manifest.is_file():
                version = version_from_manifest(manifest.read_text(encoding="utf-8", errors="replace"))
                if version:
                    return version
            log = d / "Game.log"
            if log.is_file():
                with log.open(encoding="utf-8", errors="replace") as f:
                    version = version_from_log(line for _, line in zip(range(200), f))
                if version:
                    return version
        except OSError:
            continue
    return ""


def channel_from_path(path: Optional[str]) -> str:
    """Star-Citizen-Channel aus dem Installationspfad.

    ``...\\StarCitizen\\LIVE\\Bin64\\StarCitizen.exe`` → ``LIVE`` (ebenso PTU,
    EPTU, HOTFIX, TECH-PREVIEW). Andere Spiele ohne ``Bin64``-Ordner → ``""``.
    ``PureWindowsPath`` trennt an ``\\`` und ``/``, passt also auch für Linux-Pfade.
    """
    if not path:
        return ""
    p = PureWindowsPath(path)
    if p.parent.name.lower() == "bin64" and p.parent.parent.name:
        return p.parent.parent.name.upper()
    return ""


# --- Linux (/proc) ------------------------------------------------------------


def basename_any(path: str) -> str:
    """Letzter Pfadteil, egal ob mit ``/`` oder ``\\`` getrennt."""
    return path.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]


def argv0(cmdline: bytes) -> str:
    """Erstes Argument aus ``/proc/<pid>/cmdline`` (NUL-getrennt)."""
    return cmdline.split(b"\0", 1)[0].decode("utf-8", "replace")


def start_from_stat(stat: str, boot_time: float, ticks_per_s: float) -> Optional[float]:
    """Startzeit (Unix) aus ``/proc/<pid>/stat``: Feld 22 = Takte seit Systemstart.

    Der Prozessname (Feld 2) steht in Klammern und darf Leerzeichen enthalten,
    daher erst hinter der letzten ``)`` zerlegen.
    """
    try:
        fields = stat.rsplit(")", 1)[1].split()
        return boot_time + int(fields[19]) / ticks_per_s
    except (IndexError, ValueError):
        return None


def _read(path: str, binary: bool = False):
    try:
        with open(path, "rb" if binary else "r") as f:
            return f.read()
    except OSError:
        return None


def _linux_names(pid: str) -> set[str]:
    names: set[str] = set()
    cmd = _read(f"/proc/{pid}/cmdline", binary=True)
    if cmd:
        names.add(basename_any(argv0(cmd)).lower())
    comm = _read(f"/proc/{pid}/comm")
    if comm:
        names.add(comm.strip().lower())  # vom Kernel auf 15 Zeichen gekürzt
    try:
        names.add(os.path.basename(os.readlink(f"/proc/{pid}/exe")).lower())
    except OSError:
        pass
    return names


def _linux_find(exe_names: Iterable[str]) -> dict[str, int]:
    wanted = {n.lower() for n in exe_names}
    found: dict[str, int] = {}
    if not wanted:
        return found
    try:
        pids = [e.name for e in os.scandir("/proc") if e.name.isdigit()]
    except OSError:
        return found
    for pid in pids:
        for name in _linux_names(pid) & wanted:
            found.setdefault(name, int(pid))
        if len(found) == len(wanted):
            break
    return found


def _linux_image_path(pid: int) -> Optional[str]:
    cmd = _read(f"/proc/{pid}/cmdline", binary=True)
    if cmd:
        first = argv0(cmd)
        if "/" in first or "\\" in first:  # bei Wine der Windows-Pfad mit Channel
            return first
    try:
        return os.readlink(f"/proc/{pid}/exe")
    except OSError:
        return None


def _linux_start_time(pid: int) -> Optional[float]:
    stat = _read(f"/proc/{pid}/stat")
    boot = _read("/proc/stat")
    if not stat or not boot:
        return None
    btime = next((line.split()[1] for line in boot.splitlines() if line.startswith("btime ")), None)
    if btime is None:
        return None
    return start_from_stat(stat, float(btime), float(os.sysconf("SC_CLK_TCK")))


def _linux_version(pid: int) -> str:
    # Unter Wine ist der Programmpfad ein Windows-Pfad; das Arbeitsverzeichnis
    # (meist …/LIVE/Bin64) liegt dagegen als echter Linux-Pfad vor.
    dirs: list[Path] = []
    try:
        cwd = Path(os.readlink(f"/proc/{pid}/cwd"))
        dirs += [cwd, cwd.parent]
    except OSError:
        pass
    image = _linux_image_path(pid)
    if image and image.startswith("/"):
        dirs.append(Path(image).parent.parent)
    return version_in_dirs(dirs)


_linux_xss = None  # ctypes-Handles für XScreenSaver, False = nicht verfügbar


def _linux_idle() -> Optional[float]:
    """Sekunden seit der letzten Eingabe über die XScreenSaver-Erweiterung (X11/XWayland)."""
    global _linux_xss
    if _linux_xss is None:
        _linux_xss = False
        try:
            import ctypes
            import ctypes.util

            class _Info(ctypes.Structure):
                _fields_ = [("window", ctypes.c_ulong), ("state", ctypes.c_int), ("kind", ctypes.c_int),
                            ("til_or_since", ctypes.c_ulong), ("idle", ctypes.c_ulong),
                            ("event_mask", ctypes.c_ulong)]

            x11 = ctypes.cdll.LoadLibrary(ctypes.util.find_library("X11") or "libX11.so.6")
            xss = ctypes.cdll.LoadLibrary(ctypes.util.find_library("Xss") or "libXss.so.1")
            x11.XOpenDisplay.restype = ctypes.c_void_p
            x11.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
            x11.XDefaultRootWindow.restype = ctypes.c_ulong
            xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(_Info)
            xss.XScreenSaverQueryInfo.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_Info)]
            display = x11.XOpenDisplay(None)
            if display:
                _linux_xss = (xss, display, x11.XDefaultRootWindow(display), xss.XScreenSaverAllocInfo())
        except (OSError, AttributeError):
            pass
    if not _linux_xss:
        return None
    xss, display, root, info = _linux_xss
    if not xss.XScreenSaverQueryInfo(display, root, info):
        return None
    return info.contents.idle / 1000.0


# --- Windows (Win32 über ctypes) ---------------------------------------------

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    _TH32CS_SNAPPROCESS = 0x00000002
    _PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    _INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
    # 100-ns-Intervalle zwischen 1601-01-01 (FILETIME) und 1970-01-01 (Unix)
    _EPOCH_DIFF = 116_444_736_000_000_000

    class _PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.c_size_t),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", wintypes.WCHAR * 260),
        ]

    _kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    _kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    _kernel32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PROCESSENTRY32W)]
    _kernel32.Process32FirstW.restype = wintypes.BOOL
    _kernel32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PROCESSENTRY32W)]
    _kernel32.Process32NextW.restype = wintypes.BOOL
    _kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenProcess.restype = wintypes.HANDLE
    _kernel32.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    _kernel32.GetProcessTimes.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.QueryFullProcessImageNameW.argtypes = [
        wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)
    ]
    _kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL

    def _win_find(exe_names: Iterable[str]) -> dict[str, int]:
        wanted = {n.lower() for n in exe_names}
        found: dict[str, int] = {}
        if not wanted:
            return found
        snap = _kernel32.CreateToolhelp32Snapshot(_TH32CS_SNAPPROCESS, 0)
        if not snap or snap == _INVALID_HANDLE_VALUE:
            return found
        try:
            entry = _PROCESSENTRY32W()
            entry.dwSize = ctypes.sizeof(_PROCESSENTRY32W)
            ok = _kernel32.Process32FirstW(snap, ctypes.byref(entry))
            while ok:
                name = entry.szExeFile.lower()
                if name in wanted and name not in found:
                    found[name] = int(entry.th32ProcessID)
                ok = _kernel32.Process32NextW(snap, ctypes.byref(entry))
            return found
        finally:
            _kernel32.CloseHandle(snap)

    def _win_image_path(pid: int) -> Optional[str]:
        handle = _kernel32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return None
        try:
            size = wintypes.DWORD(1024)
            buf = ctypes.create_unicode_buffer(size.value)
            if not _kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
                return None
            return buf.value
        finally:
            _kernel32.CloseHandle(handle)

    def _win_start_time(pid: int) -> Optional[float]:
        handle = _kernel32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return None
        try:
            created, exited, kernel, user = (wintypes.FILETIME() for _ in range(4))
            if not _kernel32.GetProcessTimes(
                handle, ctypes.byref(created), ctypes.byref(exited), ctypes.byref(kernel), ctypes.byref(user)
            ):
                return None
            ticks = (created.dwHighDateTime << 32) | created.dwLowDateTime
            return (ticks - _EPOCH_DIFF) / 10_000_000
        finally:
            _kernel32.CloseHandle(handle)

    def _win_version(pid: int) -> str:
        image = _win_image_path(pid)
        if not image:
            return ""
        p = Path(image)
        return version_in_dirs([p.parent.parent, p.parent])  # …\LIVE\ bzw. …\LIVE\Bin64\

    class _LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]

    _user32 = ctypes.WinDLL("user32")
    _user32.GetLastInputInfo.argtypes = [ctypes.POINTER(_LASTINPUTINFO)]
    _user32.GetLastInputInfo.restype = wintypes.BOOL
    _kernel32.GetTickCount.restype = wintypes.DWORD

    def _win_idle() -> Optional[float]:
        """Sekunden seit der letzten Tastatur-/Maus-/Controller-Eingabe am PC."""
        info = _LASTINPUTINFO()
        info.cbSize = ctypes.sizeof(_LASTINPUTINFO)
        if not _user32.GetLastInputInfo(ctypes.byref(info)):
            return None
        # beide Werte sind 32-Bit-Millisekunden und laufen nach ~49 Tagen über
        return ((_kernel32.GetTickCount() - info.dwTime) & 0xFFFFFFFF) / 1000.0

    find_processes = _win_find
    process_image_path = _win_image_path
    process_start_time = _win_start_time
    process_version = _win_version
    idle_seconds = _win_idle
else:
    find_processes = _linux_find
    process_image_path = _linux_image_path
    process_start_time = _linux_start_time
    process_version = _linux_version
    idle_seconds = _linux_idle
