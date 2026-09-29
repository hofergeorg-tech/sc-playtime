"""Prozess-Erkennung über die Win32-API (ctypes, keine Zusatzpakete).

Nur lesend: Prozessliste per Toolhelp-Snapshot und die Startzeit des Prozesses
per ``GetProcessTimes`` — nichts, was ein Anti-Cheat stören sollte.
"""

from __future__ import annotations

import ctypes
from ctypes import wintypes
from pathlib import PureWindowsPath
from typing import Iterable, Optional

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


def find_processes(exe_names: Iterable[str]) -> dict[str, int]:
    """Ein Snapshot für alle gesuchten EXEs → {exe_name_lower: pid}."""
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


def process_image_path(pid: int) -> Optional[str]:
    """Vollständiger Pfad der EXE, None falls nicht lesbar."""
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


def channel_from_path(path: Optional[str]) -> str:
    """Star-Citizen-Channel aus dem Installationspfad.

    ``...\\StarCitizen\\LIVE\\Bin64\\StarCitizen.exe`` → ``LIVE`` (ebenso PTU,
    EPTU, HOTFIX, TECH-PREVIEW). Andere Spiele ohne ``Bin64``-Ordner → ``""``.
    """
    if not path:
        return ""
    p = PureWindowsPath(path)
    if p.parent.name.lower() == "bin64" and p.parent.parent.name:
        return p.parent.parent.name.upper()
    return ""


def process_start_time(pid: int) -> Optional[float]:
    """Startzeit des Prozesses als Unix-Zeitstempel, None falls nicht lesbar."""
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
