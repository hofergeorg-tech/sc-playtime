"""Fenster für Hilfe und Changelog (Markdown aus HILFE.md / CHANGELOG.md)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

from . import __version__

DOC_QSS = """
QDialog { background: #08111b; }
QTextBrowser {
    background: #0a131d; border: 1px solid #1f4255; color: #cfe6f5;
    font-family: 'Bahnschrift', 'Segoe UI'; font-size: 13px; padding: 10px;
    selection-background-color: #12455f;
}
QScrollBar:vertical { background: #0a131d; width: 10px; }
QScrollBar::handle:vertical { background: #1f4255; min-height: 30px; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; }
"""

# Tabellenköpfe und Code passend zum HUD einfärben (Linkfarbe kommt aus der Palette)
_DOC_CSS = "th { color: #5fd0ff; } code { color: #64ffb4; }"

_open: dict[str, "DocDialog"] = {}


def resource(name: str) -> Path:
    """Datei im Projektordner bzw. im entpackten PyInstaller-Ordner (build.py packt sie ein)."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base / name


class DocDialog(QtWidgets.QDialog):
    def __init__(self, title: str, markdown: str) -> None:
        super().__init__(None, QtCore.Qt.WindowType.Window)
        self.setWindowTitle(f"SC Playtime {__version__} – {title}")
        self.setStyleSheet(DOC_QSS)
        self.resize(640, 720)
        view = QtWidgets.QTextBrowser()
        # Links selbst behandeln: "#abschnitt" springt zur Überschrift, alles andere in den Browser
        view.setOpenLinks(False)
        view.anchorClicked.connect(self._follow)
        view.document().setDefaultStyleSheet(_DOC_CSS)
        view.setMarkdown(markdown)
        _color_links(view.document(), QtGui.QColor("#5fd0ff"))
        self._view = view
        close = QtWidgets.QPushButton("Schließen")
        close.clicked.connect(self.close)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(view)
        lay.addWidget(close, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

    def _follow(self, url: QtCore.QUrl) -> None:
        if url.scheme() in ("http", "https"):
            QtGui.QDesktopServices.openUrl(url)
            return
        target = url.fragment()
        block = self._view.document().begin()
        while block.isValid():
            if block.blockFormat().headingLevel() and slug(block.text()) == target:
                cursor = QtGui.QTextCursor(block)
                self._view.setTextCursor(cursor)
                bar = self._view.verticalScrollBar()
                bar.setValue(int(self._view.document().documentLayout().blockBoundingRect(block).top()))
                return
            block = block.next()


def _color_links(doc: QtGui.QTextDocument, color: QtGui.QColor) -> None:
    """Der Markdown-Import färbt Links fest dunkelblau; auf dunklem Grund unlesbar."""
    fmt = QtGui.QTextCharFormat()
    fmt.setForeground(color)
    block = doc.begin()
    while block.isValid():
        it = block.begin()
        while not it.atEnd():
            frag = it.fragment()
            if frag.isValid() and frag.charFormat().isAnchor():
                cursor = QtGui.QTextCursor(doc)
                cursor.setPosition(frag.position())
                cursor.setPosition(frag.position() + frag.length(), QtGui.QTextCursor.MoveMode.KeepAnchor)
                cursor.mergeCharFormat(fmt)
            it += 1
        block = block.next()


def slug(heading: str) -> str:
    """GitHub-Anker einer Überschrift: "Channels (LIVE, PTU, …)" → "channels-live-ptu-"."""
    return "".join(c for c in heading.strip().lower().replace(" ", "-") if c.isalnum() or c in "-_")


def show_doc(file: str, title: str, markdown: Optional[str] = None) -> None:
    """Zeigt die Datei (oder übergebenen Text) nicht-modal; ein Fenster je Titel."""
    dlg = _open.get(title)
    if dlg is None or not dlg.isVisible():
        if markdown is None:
            try:
                markdown = resource(file).read_text(encoding="utf-8")
            except OSError:
                markdown = f"*{file} nicht gefunden.*"
        dlg = DocDialog(title, markdown)
        dlg.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        dlg.destroyed.connect(lambda _o=None, t=title: _open.pop(t, None))
        _open[title] = dlg
    dlg.show()
    dlg.raise_()
    dlg.activateWindow()


def show_help() -> None:
    show_doc("HILFE.md", "Hilfe")


def show_changelog() -> None:
    show_doc("CHANGELOG.md", "Was ist neu?")
