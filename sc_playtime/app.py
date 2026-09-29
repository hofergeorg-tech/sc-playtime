"""Einstiegspunkt: Tracker, Overlay und Tray-Icon verdrahten."""

from __future__ import annotations

import sys

from PySide6 import QtCore, QtGui, QtWidgets

from .settings import Settings, data_dir
from .store import Store
from .tracker import Tracker
from .ui import MENU_QSS, Overlay, app_icon

POLL_MS = 2000


def main() -> int:
    QtGui.QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("SC Playtime")
    app.setStyleSheet(MENU_QSS)

    folder = data_dir()
    # Autostart + manueller Start dürfen nicht doppelt zählen
    lock = QtCore.QLockFile(str(folder / "instance.lock"))
    if not lock.tryLock(100):
        return 0

    settings_path = folder / "settings.json"
    settings = Settings.load(settings_path)
    store = Store(folder / "playtime.db")
    tracker = Tracker(store, settings.game_list())
    tracker.poll()

    overlay = Overlay(tracker, settings, lambda: settings.save(settings_path))
    overlay.games_changed.connect(lambda: tracker.set_games(settings.game_list()))

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

    def poll() -> None:
        tracker.poll()

    timer = QtCore.QTimer(interval=POLL_MS, timeout=poll)
    timer.start()

    def shutdown() -> None:
        tracker.flush()
        store.close()
        lock.unlock()

    app.aboutToQuit.connect(shutdown)
    overlay.refresh()
    return app.exec()
