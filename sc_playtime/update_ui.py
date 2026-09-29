"""Update-Ablauf in der Oberfläche: Prüfen im Hintergrund, Hinweis, Installieren."""

from __future__ import annotations

import threading
from typing import Callable, Optional

from PySide6 import QtCore, QtGui, QtWidgets

from . import __version__, updater
from .i18n import tr
from .settings import Settings

CHECK_EVERY_MS = 12 * 3600 * 1000
FIRST_CHECK_MS = 15 * 1000  # nicht direkt beim Windows-Login, Netz ist evtl. noch nicht da


class UpdateManager(QtCore.QObject):
    # aus dem Hintergrund-Thread gesendet → Qt stellt sie in den GUI-Thread zu
    _checked = QtCore.Signal(object, object, bool)  # Release | None, Fehler | None, manuell
    _downloaded = QtCore.Signal(object, object)  # Pfad | None, Fehler | None

    def __init__(self, settings: Settings, save: Callable[[], None], notify: Callable[[str, str], None],
                 parent: Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self._s = settings
        self._save = save
        self._notify = notify
        self._busy = False
        self._notified = ""
        self._progress: Optional[QtWidgets.QProgressDialog] = None
        self.available: Optional[updater.Release] = None
        self._checked.connect(self._on_checked)
        self._downloaded.connect(self._on_downloaded)
        self._timer = QtCore.QTimer(self, interval=CHECK_EVERY_MS, timeout=self._auto_check)
        self._timer.start()
        QtCore.QTimer.singleShot(FIRST_CHECK_MS, self._auto_check)

    # --- Prüfen -------------------------------------------------------------

    def _auto_check(self) -> None:
        if self._s.auto_update:
            self.check(manual=False)

    def check(self, manual: bool = True) -> None:
        if self._busy:
            return
        self._busy = True

        def run() -> None:
            try:
                self._checked.emit(updater.fetch_latest(), None, manual)
            except Exception as exc:  # Netzfehler dürfen die App nie stören
                self._checked.emit(None, exc, manual)

        threading.Thread(target=run, daemon=True).start()

    def _on_checked(self, release: Optional[updater.Release], error: Optional[Exception], manual: bool) -> None:
        self._busy = False
        if error is not None or release is None:
            if manual:
                _message(QtWidgets.QMessageBox.Icon.Warning, tr("upd.check_failed_title"),
                         tr("upd.unreachable", error=error))
            return
        if updater.is_newer(release.version):
            self.available = release
            if manual:
                self.install()
            elif self._notified != release.version:
                self._notified = release.version
                self._notify(tr("upd.available_title"),
                             tr("upd.notify", new=release.version, current=__version__))
        else:
            self.available = None
            if manual:
                _message(QtWidgets.QMessageBox.Icon.Information, tr("upd.none_title"),
                         tr("upd.none", version=__version__))

    # --- Installieren -------------------------------------------------------

    def install(self) -> None:
        rel = self.available
        if rel is None or self._busy:
            return
        box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question, tr("upd.available_title"),
                                    tr("upd.question", new=rel.version, current=__version__))
        box.setInformativeText(tr("upd.confirm_self" if self._can_self_update(rel) else "upd.confirm_browser"))
        if rel.notes:
            box.setDetailedText(rel.notes)
        box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if box.exec() != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        if not self._can_self_update(rel):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(rel.page_url))
            return

        self._busy = True
        self._progress = QtWidgets.QProgressDialog(tr("upd.downloading"), "", 0, 0)
        self._progress.setWindowTitle("SC Playtime")
        self._progress.setCancelButton(None)
        self._progress.setMinimumDuration(0)
        self._progress.show()

        url = rel.exe_url

        def run() -> None:
            try:
                self._downloaded.emit(updater.download(url), None)
            except Exception as exc:
                self._downloaded.emit(None, exc)

        threading.Thread(target=run, daemon=True).start()

    @staticmethod
    def _can_self_update(rel: updater.Release) -> bool:
        return updater.is_frozen() and rel.exe_url is not None

    def _on_downloaded(self, path, error: Optional[Exception]) -> None:
        self._busy = False
        if self._progress is not None:
            self._progress.close()
            self._progress = None
        if error is not None or path is None:
            _message(QtWidgets.QMessageBox.Icon.Warning, tr("upd.failed_title"),
                     tr("upd.download_failed", error=error))
            return
        try:
            updater.start_install(path)
        except OSError as exc:
            _message(QtWidgets.QMessageBox.Icon.Warning, tr("upd.failed_title"), str(exc))
            return
        QtWidgets.QApplication.quit()

    # --- Menü ---------------------------------------------------------------

    def add_install_action(self, menu: QtWidgets.QMenu) -> None:
        """Hervorgehobener Eintrag, nur wenn ein Update bereitliegt."""
        if self.available is None:
            return
        act = menu.addAction(tr("menu.install_update", version=self.available.version), self.install)
        f = act.font()
        f.setBold(True)
        act.setFont(f)

    def populate_menu(self, menu: QtWidgets.QMenu) -> None:
        menu.addAction(tr("menu.check_updates"), lambda: self.check(manual=True))
        act = menu.addAction(tr("menu.auto_update"))
        act.setCheckable(True)
        act.setChecked(self._s.auto_update)
        act.toggled.connect(self._set_auto)

    def _set_auto(self, on: bool) -> None:
        self._s.auto_update = on
        self._save()
        if on:
            self.check(manual=False)


def _message(icon: QtWidgets.QMessageBox.Icon, title: str, text: str) -> None:
    QtWidgets.QMessageBox(icon, title, text).exec()
