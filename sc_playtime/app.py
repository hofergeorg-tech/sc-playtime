"""Einstiegspunkt: Tracker, Overlay und Tray-Icon verdrahten."""

from __future__ import annotations

import os
import sqlite3
import sys
from datetime import date

from PySide6 import QtCore, QtGui, QtWidgets

from . import __version__, backup, docs, i18n
from .hotkeys import Hotkeys
from .settings import Settings, data_dir
from .store import Store
from .tracker import Tracker
from .ui import MENU_QSS, Overlay, TopmostPopups, app_icon, apply_qt_language
from .update_ui import UpdateManager
from .updater import is_newer

POLL_MS = 2000
BACKUP_CHECK_MS = 3600 * 1000  # stündlich prüfen, ob für heute schon gesichert wurde
HOTKEY_TOGGLE, HOTKEY_CLICK = 1, 2


class _HotkeyBridge(QtCore.QObject):
    """Bringt Tastenkürzel aus dem Hotkey-Thread in den GUI-Thread."""

    fired = QtCore.Signal(int)


def main() -> int:
    if sys.platform.startswith("linux"):
        # Unter Wayland darf ein Fenster weder seine Position bestimmen noch
        # "immer oben" bleiben → über XWayland (xcb) laufen, sonst Wayland.
        os.environ.setdefault("QT_QPA_PLATFORM", "xcb;wayland")
    QtGui.QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("SC Playtime")
    app.setStyleSheet(MENU_QSS)
    topmost = TopmostPopups(app)
    app.installEventFilter(topmost)

    folder = data_dir()
    # Autostart + manueller Start dürfen nicht doppelt zählen
    lock = QtCore.QLockFile(str(folder / "instance.lock"))
    if not lock.tryLock(100):
        return 0

    settings_path = folder / "settings.json"
    settings = Settings.load(settings_path)
    i18n.set_language(settings.language)
    apply_qt_language()
    store = Store(folder / "playtime.db")
    tracker = Tracker(store, settings.game_list(), afk_s=settings.afk_minutes * 60.0)
    tracker.poll()

    overlay = Overlay(tracker, settings, lambda: settings.save(settings_path))
    overlay.games_changed.connect(lambda: tracker.set_games(settings.game_list()))

    backups = backup.backup_dir(folder)
    overlay.backup_now = lambda: backup.run(store, backups, date.today(), force=True)

    def daily_backup() -> None:
        if settings.auto_backup:
            try:
                backup.run(store, backups, date.today())
            except (OSError, sqlite3.Error):
                pass  # nächster Versuch in einer Stunde

    daily_backup()
    backup_timer = QtCore.QTimer(interval=BACKUP_CHECK_MS, timeout=daily_backup)
    backup_timer.start()

    bridge = _HotkeyBridge()
    bridge.fired.connect(lambda hid: overlay.toggle_hidden() if hid == HOTKEY_TOGGLE
                         else overlay.toggle_click_through() if hid == HOTKEY_CLICK else None)
    hotkeys = Hotkeys(bridge.fired.emit)
    overlay.apply_hotkeys = lambda: hotkeys.set({HOTKEY_TOGGLE: settings.hotkey_toggle,
                                                 HOTKEY_CLICK: settings.hotkey_click})
    overlay.apply_hotkeys()

    tray = QtWidgets.QSystemTrayIcon(app_icon(), app)
    tray_menu = QtWidgets.QMenu()

    def rebuild_tray_menu() -> None:
        tray_menu.clear()
        overlay.populate_menu(tray_menu, tray=True)

    tray_menu.aboutToShow.connect(rebuild_tray_menu)
    rebuild_tray_menu()
    tray.setContextMenu(tray_menu)
    tray.activated.connect(
        lambda reason: overlay.toggle_hidden()
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger
        else None
    )
    overlay.on_status = tray.setToolTip
    tray.show()

    updates = UpdateManager(
        settings, lambda: settings.save(settings_path),
        lambda title, text: tray.showMessage(title, text, app_icon(), 15000), app,
    )
    overlay.updates = updates
    tray.messageClicked.connect(updates.install)

    # nach einem Update einmal zeigen, was neu ist (nicht beim allerersten Start)
    if settings.seen_version != __version__:
        if settings.seen_version and is_newer(__version__, settings.seen_version):
            QtCore.QTimer.singleShot(1500, docs.show_changelog)
        settings.seen_version = __version__
        settings.save(settings_path)

    def poll() -> None:
        tracker.poll()

    timer = QtCore.QTimer(interval=POLL_MS, timeout=poll)
    timer.start()

    def shutdown() -> None:
        hotkeys.stop()
        tracker.flush()
        store.close()
        lock.unlock()

    app.aboutToQuit.connect(shutdown)
    overlay.refresh()
    return app.exec()
