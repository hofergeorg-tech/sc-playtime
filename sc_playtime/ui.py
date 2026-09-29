"""Das Overlay: rahmenloses HUD-Panel im Star-Citizen-Stil, komplett selbst gezeichnet.

Kompakt: Spiel + Channel, laufende Session als große Uhr, Heute/Woche.
Erweitert (Klick auf den Kopf): Channel-Filter, Kacheln, Balkendiagramm
Tag/Woche/Monat/Jahr mit Hover-Werten.
"""

from __future__ import annotations

import ctypes
import math
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Optional

from PySide6 import QtCore, QtGui, QtWidgets

from . import __version__, autostart, docs
from .settings import Settings, data_dir
from .stats import BUCKET_COUNT, Bucket, Summary, buckets, fmt_clock, fmt_hm, played, summarize
from .tracker import Tracker

if TYPE_CHECKING:
    from .update_ui import UpdateManager

Qt = QtCore.Qt
QRectF = QtCore.QRectF
QPointF = QtCore.QPointF

CYAN = (95, 208, 255)
GREEN = (100, 255, 180)
AMBER = (255, 196, 90)
TEXT = (226, 243, 255)
MUTED = (112, 150, 175)
DIM = (70, 100, 122)

# Farbe je Star-Citizen-Channel (Chip im Kopf + Filter)
CHANNEL_COLORS = {
    "LIVE": GREEN,
    "PTU": AMBER,
    "EPTU": (255, 150, 80),
    "HOTFIX": (255, 110, 110),
    "TECH-PREVIEW": (190, 140, 255),
}

# Farbvorlagen für den aktiven Channel-Chip: (Menütext, Hintergrund, Schrift)
CHIP_PRESETS = (
    ("Automatisch (Channel-Farbe, dunkle Schrift)", "", ""),
    ("Dunkelgrün / Weiß", "#0f5132", "#ffffff"),
    ("Schwarz / Grün", "#05140c", "#64ffb4"),
    ("Dunkelblau / Weiß", "#0b2a44", "#ffffff"),
    ("Weiß / Schwarz", "#f2f2f2", "#000000"),
)

# Farbvorlagen für die Statistik-Kacheln bei laufendem Spiel (offline immer HUD-dunkel)
TILE_PRESETS = (
    ("Grün / Dunkel", "#64ffb4", "#04141a"),
    ("Cyan / Dunkel", "#5fd0ff", "#04141a"),
    ("Bernstein / Dunkel", "#ffc45a", "#04141a"),
    ("Nicht einfärben (HUD)", "", ""),
)

W = 320
H_COMPACT = 78
PAD = 12
TABS = (("day", "TAG"), ("week", "WOCHE"), ("month", "MONAT"), ("year", "JAHR"), ("total", "GESAMT"))

MENU_QSS = """
QMenu {
    background: #08111b; border: 1px solid #2a6f8f; color: #cfe6f5;
    padding: 6px; font-family: 'Bahnschrift', 'Segoe UI'; font-size: 12px;
}
QMenu::item { padding: 6px 24px 6px 24px; }
QMenu::item:selected { background: #12455f; color: #eaffff; }
QMenu::item:disabled { color: #5fd0ff; font-weight: 700; letter-spacing: 2px; }
QMenu::separator { height: 1px; background: #1f4255; margin: 5px 8px; }
QMenu QLabel { color: #6f93a8; font-size: 10px; letter-spacing: 1px; background: transparent; }
QMenu QWidget { background: transparent; }
QSlider::groove:horizontal { height: 4px; background: #16303f; border-radius: 2px; }
QSlider::sub-page:horizontal { background: #5fd0ff; border-radius: 2px; }
QSlider::handle:horizontal {
    background: #eaffff; border: 1px solid #5fd0ff; width: 10px; margin: -5px 0; border-radius: 5px;
}
QInputDialog, QMessageBox { background: #08111b; color: #cfe6f5; }
QLineEdit { background: #0a131d; border: 1px solid #1f4255; padding: 4px 7px; color: #e3f4ff; }
QPushButton {
    background: #102232; border: 1px solid #2a6f8f; padding: 5px 14px; color: #bfe9ff;
}
QPushButton:hover { background: #16384f; border-color: #45b6e0; }
"""


def rgba(c: tuple[int, int, int], a: int = 255) -> QtGui.QColor:
    return QtGui.QColor(c[0], c[1], c[2], max(0, min(255, int(a))))


_FAMILY: Optional[str] = None


def font(px: int, weight: QtGui.QFont.Weight = QtGui.QFont.Weight.Normal, spacing: float = 0.0) -> QtGui.QFont:
    global _FAMILY
    if _FAMILY is None:
        fams = set(QtGui.QFontDatabase.families())
        _FAMILY = next((f for f in ("Bahnschrift", "Segoe UI") if f in fams), QtWidgets.QApplication.font().family())
    f = QtGui.QFont(_FAMILY)
    f.setPixelSize(px)
    f.setWeight(weight)
    if spacing:
        f.setLetterSpacing(QtGui.QFont.SpacingType.AbsoluteSpacing, spacing)
    return f


def chamfer(r: QRectF, c: float) -> QtGui.QPainterPath:
    """Rechteck mit abgeschrägter Ecke oben links und unten rechts (SC-HUD-Look)."""
    p = QtGui.QPainterPath()
    p.moveTo(r.left() + c, r.top())
    p.lineTo(r.right(), r.top())
    p.lineTo(r.right(), r.bottom() - c)
    p.lineTo(r.right() - c, r.bottom())
    p.lineTo(r.left(), r.bottom())
    p.lineTo(r.left(), r.top() + c)
    p.closeSubpath()
    return p


def app_icon() -> QtGui.QIcon:
    pm = QtGui.QPixmap(64, 64)
    pm.fill(Qt.GlobalColor.transparent)
    p = QtGui.QPainter(pm)
    p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
    path = chamfer(QRectF(4, 4, 56, 56), 14)
    p.fillPath(path, rgba((8, 20, 32)))
    p.setPen(QtGui.QPen(rgba(CYAN), 4))
    p.drawPath(path)
    hand = QtGui.QPen(rgba(TEXT), 5)
    hand.setCapStyle(Qt.PenCapStyle.RoundCap)
    p.setPen(hand)
    p.drawLine(QPointF(32, 32), QPointF(32, 17))
    p.drawLine(QPointF(32, 32), QPointF(43, 38))
    p.end()
    return QtGui.QIcon(pm)


@dataclass
class _Layout:
    height: float
    chips: list[tuple[str, QRectF]] = field(default_factory=list)
    tiles: list[QRectF] = field(default_factory=list)
    tabs: list[tuple[str, str, QRectF]] = field(default_factory=list)
    chart: QRectF = field(default_factory=QRectF)
    footer_y: float = 0.0


class Overlay(QtWidgets.QWidget):
    games_changed = QtCore.Signal()

    def __init__(self, tracker: Tracker, settings: Settings, save: Callable[[], None]) -> None:
        super().__init__()
        self._tracker = tracker
        self._s = settings
        self._save = save
        self._user_hidden = False
        self._press: Optional[tuple[QtCore.QPoint, QtCore.QPoint]] = None
        self._moved = False
        self._hover: Optional[int] = None
        self._ticks = 0
        # Anzeige-Zustand, einmal pro Sekunde neu berechnet (paintEvent läuft
        # wegen der Puls-Animation öfter und soll nichts rechnen).
        self._game = settings.game
        self._running = False
        self._live_channel: Optional[str] = None
        self._channels: list[str] = []
        self._duration = 0.0
        self._summary: Optional[Summary] = None
        self._bars: list[tuple[Bucket, float]] = []
        self.on_status: Callable[[str], None] = lambda _t: None
        self.updates: Optional["UpdateManager"] = None  # von app.py gesetzt

        self.setWindowTitle("SC Playtime")
        self.setWindowIcon(app_icon())
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setMouseTracking(True)
        self._apply_flags()
        self.setWindowOpacity(settings.opacity / 100)

        self.setFixedSize(W, H_COMPACT)
        self._place_initial()
        self.refresh()

        self._tick = QtCore.QTimer(self, interval=1000, timeout=self._on_tick)
        self._tick.start()
        self._pulse = QtCore.QTimer(self, interval=60, timeout=self._on_pulse)
        self._pulse.start()

    def _on_pulse(self) -> None:
        if self._running and self.isVisible():
            self.update(QtCore.QRect(8, 10, 24, 24))

    # --- Zustand ------------------------------------------------------------

    def _pick_game(self) -> str:
        running = self._tracker.running()
        if self._s.game in running:
            return self._s.game
        if running:
            return running[0]
        names = [g.name for g in self._s.game_list()]
        return self._s.game if self._s.game in names else (names[0] if names else "—")

    def refresh(self) -> None:
        game = self._pick_game()
        self._game = game
        self._running = game in self._tracker.running()
        self._live_channel = self._tracker.live_channel(game)
        self._channels = self._tracker.channels(game)
        channel = self._s.channel if self._s.channel in self._channels else ""
        sessions = self._tracker.sessions(game, channel)
        now = datetime.now()
        self._duration = self._tracker.current_duration(game, channel)
        self._summary = summarize(sessions, now)
        if self._s.tab == "total":
            # alle Jahre seit der ersten Session (mindestens das laufende)
            first = datetime.fromtimestamp(min(s for s, _ in sessions)).year if sessions else now.year
            kind, count = "year", now.year - first + 1
        else:
            kind = self._s.tab if self._s.tab in BUCKET_COUNT else "day"
            count = BUCKET_COUNT[kind]
        self._bars = [(b, played(sessions, b.start, b.end)) for b in buckets(kind, now.date(), count)]

        lay = self._layout()
        size = QtCore.QSize(W, int(lay.height))
        if self.size() != size:
            self.setFixedSize(size)
            self._clamp_to_screen()

        state = "AKTIV" if self._running else "offline"
        self.on_status(f"SC Playtime · {game} {state} · Heute {fmt_hm(self._summary.today)}")
        self._sync_visibility()
        self.update()

    def _on_tick(self) -> None:
        self._ticks += 1
        self.refresh()
        if self._ticks % 5 == 0:
            self._keep_on_top()

    def _sync_visibility(self) -> None:
        want = not self._user_hidden and (self._running or not self._s.hide_when_offline)
        if want != self.isVisible():
            self.setVisible(want)

    def toggle_hidden(self) -> None:
        self._user_hidden = not self._user_hidden
        self._sync_visibility()

    def _keep_on_top(self) -> None:
        # Manche Spiele im randlosen Fenstermodus schieben sich beim Fokus
        # davor; TOPMOST ohne Aktivierung erneut setzen.
        if not self.isVisible():
            return
        swp_nosize, swp_nomove, swp_noactivate = 0x0001, 0x0002, 0x0010
        ctypes.windll.user32.SetWindowPos(
            ctypes.c_void_p(int(self.winId())), ctypes.c_void_p(-1), 0, 0, 0, 0,
            swp_nosize | swp_nomove | swp_noactivate,
        )

    # --- Fenster ------------------------------------------------------------

    def _apply_flags(self) -> None:
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool
        if self._s.click_through:
            flags |= Qt.WindowType.WindowTransparentForInput
        visible = self.isVisible()
        self.setWindowFlags(flags)
        if visible:
            self.show()

    def _place_initial(self) -> None:
        s = self._s
        if s.x is not None and s.y is not None and QtGui.QGuiApplication.screenAt(QtCore.QPoint(s.x + 20, s.y + 20)):
            self.move(s.x, s.y)
        else:
            area = QtGui.QGuiApplication.primaryScreen().availableGeometry()
            self.move(area.right() - W - 24, area.top() + 24)

    def _clamp_to_screen(self) -> None:
        screen = self.screen() or QtGui.QGuiApplication.primaryScreen()
        area = screen.availableGeometry()
        x = min(max(self.x(), area.left()), area.right() - self.width() + 1)
        y = min(max(self.y(), area.top()), area.bottom() - self.height() + 1)
        if (x, y) != (self.x(), self.y()):
            self.move(x, y)

    # --- Geometrie ----------------------------------------------------------

    def _layout(self) -> _Layout:
        if not self._s.expanded:
            return _Layout(height=H_COMPACT)
        lay = _Layout(height=0)
        top = H_COMPACT + 12.0
        if self._channels:
            fm = QtGui.QFontMetricsF(font(9, QtGui.QFont.Weight.DemiBold, 1.5))
            x = float(PAD)
            for ch in ["", *self._channels]:
                w = fm.horizontalAdvance(ch or "ALLE") + 16
                lay.chips.append((ch, QRectF(x, top, w, 18)))
                x += w + 5
            top += 28
        tw = (W - 2 * PAD - 2 * 6) / 3
        for row in range(2):
            for col in range(3):
                lay.tiles.append(QRectF(PAD + col * (tw + 6), top + row * 50, tw, 44))
        top += 94 + 12
        sw = (W - 2 * PAD) / len(TABS)
        for i, (key, label) in enumerate(TABS):
            lay.tabs.append((key, label, QRectF(PAD + i * sw, top, sw, 22)))
        top += 32
        lay.chart = QRectF(PAD, top, W - 2 * PAD, 112)
        top += 112 + 16
        lay.footer_y = top + 14
        lay.height = top + 26
        return lay

    def _bar_index_at(self, pos: QPointF) -> Optional[int]:
        chart = self._layout().chart
        if not self._bars or not chart.adjusted(0, 0, 0, 16).contains(pos):
            return None
        slot = chart.width() / len(self._bars)
        return min(len(self._bars) - 1, int((pos.x() - chart.left()) / slot))

    # --- Malen --------------------------------------------------------------

    def paintEvent(self, _e: QtGui.QPaintEvent) -> None:
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        p.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
        lay = self._layout()
        self._paint_frame(p, QRectF(0.5, 0.5, W - 1, lay.height - 1))
        self._paint_header(p)
        if self._s.expanded and self._summary is not None:
            self._paint_chips(p, lay)
            self._paint_tiles(p, lay)
            self._paint_tabs(p, lay)
            self._paint_chart(p, lay)
            self._paint_footer(p, lay)
        p.end()

    def _paint_frame(self, p: QtGui.QPainter, r: QRectF) -> None:
        a = self._s.bg_alpha / 100 * 255
        path = chamfer(r, 14)
        grad = QtGui.QLinearGradient(0, r.top(), 0, r.bottom())
        grad.setColorAt(0, rgba((10, 22, 36), a))
        grad.setColorAt(1, rgba((3, 8, 14), a))
        p.fillPath(path, grad)

        # dezenter Lichtschein oben links + Scanlines
        p.save()
        p.setClipPath(path)
        glow = QtGui.QRadialGradient(QPointF(40, 10), 180)
        glow.setColorAt(0, rgba(CYAN, 0.14 * a))
        glow.setColorAt(1, rgba(CYAN, 0))
        p.fillRect(r, glow)
        p.setPen(QtGui.QPen(rgba(CYAN, 9), 1))
        y = r.top() + 2
        while y < r.bottom():
            p.drawLine(QPointF(r.left(), y), QPointF(r.right(), y))
            y += 3
        p.restore()

        p.setPen(QtGui.QPen(rgba(CYAN, 70), 1))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(path)

        # Akzente: helle Schrägkanten, Leiste oben, Klammern an den eckigen Ecken
        bright = QtGui.QPen(rgba(CYAN, 230), 2)
        p.setPen(bright)
        p.drawLine(QPointF(r.left(), r.top() + 14), QPointF(r.left() + 14, r.top()))
        p.drawLine(QPointF(r.right(), r.bottom() - 14), QPointF(r.right() - 14, r.bottom()))
        p.drawLine(QPointF(r.left() + 14, r.top()), QPointF(r.left() + 70, r.top()))
        p.drawLine(QPointF(r.right() - 70, r.bottom()), QPointF(r.right() - 14, r.bottom()))
        p.setPen(QtGui.QPen(rgba(CYAN, 160), 1.5))
        k = 8
        p.drawLine(QPointF(r.right() - k, r.top()), QPointF(r.right(), r.top()))
        p.drawLine(QPointF(r.right(), r.top()), QPointF(r.right(), r.top() + k))
        p.drawLine(QPointF(r.left(), r.bottom() - k), QPointF(r.left(), r.bottom()))
        p.drawLine(QPointF(r.left(), r.bottom()), QPointF(r.left() + k, r.bottom()))

    def _paint_header(self, p: QtGui.QPainter) -> None:
        s = self._summary
        # Status-Punkt (pulsiert, solange das Spiel läuft)
        c = QPointF(20, 21)
        if self._running:
            pulse = 0.5 + 0.5 * math.sin(time.monotonic() * 3.2)
            halo = QtGui.QRadialGradient(c, 5 + 6 * pulse)
            halo.setColorAt(0, rgba(GREEN, 150 * pulse))
            halo.setColorAt(1, rgba(GREEN, 0))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(halo)
            p.drawEllipse(c, 11, 11)
            p.setBrush(rgba(GREEN))
        else:
            p.setPen(QtGui.QPen(rgba(DIM), 1))
            p.setBrush(rgba((25, 40, 52)))
        p.drawEllipse(c, 3.5, 3.5)
        # Pinsel zurücksetzen, sonst füllt jedes spätere drawPath (Kacheln,
        # Chips) die Fläche mit dem Grün des Status-Punkts.
        p.setBrush(Qt.BrushStyle.NoBrush)

        # Spielname + Channel-Chip
        f = font(11, QtGui.QFont.Weight.DemiBold, 2.2)
        p.setFont(f)
        p.setPen(rgba(CYAN if self._running else MUTED))
        name = self._game.upper()
        name = QtGui.QFontMetricsF(f).elidedText(name, Qt.TextElideMode.ElideRight, 130)
        p.drawText(QPointF(32, 25), name)
        x = 32 + QtGui.QFontMetricsF(f).horizontalAdvance(name) + 8
        channel = self._live_channel if self._running else (self._s.channel if self._s.channel in self._channels else "")
        if channel:
            self._chip(p, QRectF(x, 13, 0, 15), channel, active=self._running, size=8)

        # Status oben rechts
        p.setFont(font(9, QtGui.QFont.Weight.DemiBold, 2))
        p.setPen(rgba(GREEN if self._running else DIM))
        p.drawText(QRectF(0, 12, W - 16, 16), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                   "IM SPIEL" if self._running else "OFFLINE")

        # große Session-Uhr
        self._paint_clock(p, fmt_clock(self._duration), QPointF(15, 64), self._running)

        # Heute / Woche rechts
        if s is not None:
            for baseline, label, value in ((46, "HEUTE", s.today), (64, "WOCHE", s.week)):
                vf = font(14, QtGui.QFont.Weight.DemiBold)
                p.setFont(vf)
                txt = fmt_hm(value)
                vw = QtGui.QFontMetricsF(vf).horizontalAdvance(txt)
                p.setPen(rgba(TEXT))
                p.drawText(QPointF(W - 16 - vw, baseline), txt)
                lf = font(8, QtGui.QFont.Weight.DemiBold, 1.8)
                p.setFont(lf)
                p.setPen(rgba(MUTED))
                lw = QtGui.QFontMetricsF(lf).horizontalAdvance(label)
                p.drawText(QPointF(W - 16 - vw - 7 - lw, baseline), label)

        # Aufklapp-Pfeil
        cx, cy = W / 2, H_COMPACT - 7
        d = -1 if self._s.expanded else 1
        p.setPen(QtGui.QPen(rgba(CYAN, 110), 1.3))
        p.drawPolyline(QtGui.QPolygonF([QPointF(cx - 5, cy - 2 * d), QPointF(cx, cy + 2 * d), QPointF(cx + 5, cy - 2 * d)]))

        if self._s.expanded:
            y = H_COMPACT + 2
            g = QtGui.QLinearGradient(PAD, 0, W - PAD, 0)
            g.setColorAt(0, rgba(CYAN, 0))
            g.setColorAt(0.5, rgba(CYAN, 120))
            g.setColorAt(1, rgba(CYAN, 0))
            p.setPen(QtGui.QPen(QtGui.QBrush(g), 1))
            p.drawLine(QPointF(PAD, y), QPointF(W - PAD, y))

    def _paint_clock(self, p: QtGui.QPainter, text: str, origin: QPointF, active: bool) -> None:
        """Ziffern in fester Breite, damit die Uhr beim Zählen nicht wackelt."""
        f = font(32, QtGui.QFont.Weight.DemiBold)
        fm = QtGui.QFontMetricsF(f)
        cell = max(fm.horizontalAdvance(d) for d in "0123456789")
        colon = fm.horizontalAdvance(":") + 2
        p.setFont(f)
        passes = [((-1, 0), rgba(CYAN, 45)), ((1, 0), rgba(CYAN, 45)), ((0, -1), rgba(CYAN, 35)),
                  ((0, 1), rgba(CYAN, 35)), ((0, 0), rgba(TEXT))] if active else [((0, 0), rgba(DIM))]
        for (dx, dy), color in passes:
            p.setPen(color)
            x = origin.x()
            for ch in text:
                w = colon if ch == ":" else cell
                p.drawText(QPointF(x + (w - fm.horizontalAdvance(ch)) / 2 + dx, origin.y() + dy), ch)
                x += w

    def _chip(self, p: QtGui.QPainter, r: QRectF, text: str, active: bool, size: int = 9) -> QRectF:
        color = CHANNEL_COLORS.get(text, CYAN)
        f = font(size, QtGui.QFont.Weight.DemiBold, 1.5)
        if r.width() == 0:
            r = QRectF(r.left(), r.top(), QtGui.QFontMetricsF(f).horizontalAdvance(text) + 12, r.height())
        path = chamfer(r, 4)
        # Aktiv: volle Farbfläche mit dunkler Schrift — helle Schrift auf
        # halbtransparentem Grün/Gelb war kaum lesbar. Beide Farben sind im
        # Menü unter "Farben" frei wählbar.
        if active:
            bg = QtGui.QColor(self._s.chip_bg) if self._s.chip_bg else rgba(color, 235)
            fg = QtGui.QColor(self._s.chip_fg) if self._s.chip_fg else rgba((4, 14, 22))
            p.fillPath(path, bg)
            p.setPen(QtGui.QPen(QtGui.QColor(self._s.chip_bg) if self._s.chip_bg else rgba(color), 1))
        else:
            fg = rgba(MUTED)
            p.fillPath(path, rgba(color, 16))
            p.setPen(QtGui.QPen(rgba(color, 90), 1))
        p.drawPath(path)
        p.setFont(f)
        p.setPen(fg)
        p.drawText(r, Qt.AlignmentFlag.AlignCenter, text)
        return r

    def _paint_chips(self, p: QtGui.QPainter, lay: _Layout) -> None:
        current = self._s.channel if self._s.channel in self._channels else ""
        for ch, r in lay.chips:
            self._chip(p, r, ch or "ALLE", active=ch == current)

    def _paint_tiles(self, p: QtGui.QPainter, lay: _Layout) -> None:
        s = self._summary
        streak = f"{s.streak} {'TAG' if s.streak == 1 else 'TAGE'}"
        items = (("HEUTE", fmt_hm(s.today)), ("WOCHE", fmt_hm(s.week)), ("MONAT", fmt_hm(s.month)),
                 ("JAHR", fmt_hm(s.year)), ("GESAMT", fmt_hm(s.total)), ("SERIE", streak))
        # Eingefärbt nur, solange das Spiel läuft; offline die dunkle HUD-Optik.
        colored = self._running
        bg = QtGui.QColor(self._s.tile_bg) if colored and self._s.tile_bg else None
        fg = QtGui.QColor(self._s.tile_fg) if colored and self._s.tile_fg else rgba(TEXT)
        label_color = QtGui.QColor(fg)
        label_color.setAlpha(170)
        if not (colored and self._s.tile_fg):
            label_color = rgba(MUTED)
        for r, (label, value) in zip(lay.tiles, items):
            path = chamfer(r, 6)
            if bg is not None:
                p.fillPath(path, bg)
                p.setPen(QtGui.QPen(bg, 1))
                p.drawPath(path)
            else:
                g = QtGui.QLinearGradient(0, r.top(), 0, r.bottom())
                g.setColorAt(0, rgba(CYAN, 26))
                g.setColorAt(1, rgba(CYAN, 6))
                p.fillPath(path, g)
                p.setPen(QtGui.QPen(rgba(CYAN, 45), 1))
                p.drawPath(path)
                p.setPen(QtGui.QPen(rgba(CYAN, 200), 2))
                p.drawLine(QPointF(r.left() + 1, r.top() + 12), QPointF(r.left() + 1, r.bottom() - 10))
            p.setFont(font(8, QtGui.QFont.Weight.DemiBold, 1.8))
            p.setPen(label_color)
            p.drawText(QPointF(r.left() + 9, r.top() + 16), label)
            p.setFont(font(15, QtGui.QFont.Weight.DemiBold))
            p.setPen(fg)
            p.drawText(QPointF(r.left() + 9, r.top() + 36), value)

    def _paint_tabs(self, p: QtGui.QPainter, lay: _Layout) -> None:
        p.setFont(font(9, QtGui.QFont.Weight.DemiBold, 2))
        for key, label, r in lay.tabs:
            active = key == self._s.tab
            if active:
                g = QtGui.QLinearGradient(0, r.top(), 0, r.bottom())
                g.setColorAt(0, rgba(CYAN, 10))
                g.setColorAt(1, rgba(CYAN, 45))
                p.fillRect(r, g)
                p.setPen(QtGui.QPen(rgba(CYAN, 240), 2))
                p.drawLine(QPointF(r.left() + 4, r.bottom()), QPointF(r.right() - 4, r.bottom()))
            else:
                p.setPen(QtGui.QPen(rgba(CYAN, 30), 1))
                p.drawLine(QPointF(r.left() + 4, r.bottom()), QPointF(r.right() - 4, r.bottom()))
            p.setPen(rgba(CYAN if active else MUTED))
            p.drawText(r, Qt.AlignmentFlag.AlignCenter, label)

    def _paint_chart(self, p: QtGui.QPainter, lay: _Layout) -> None:
        chart = lay.chart
        values = [v for _, v in self._bars]
        vmax = max(values, default=0.0)
        top = chart.top() + 14
        base = chart.bottom()
        span = base - top

        p.setPen(QtGui.QPen(rgba(CYAN, 22), 1, Qt.PenStyle.DashLine))
        for k in (1 / 3, 2 / 3, 1.0):
            y = base - span * k
            p.drawLine(QPointF(chart.left(), y), QPointF(chart.right(), y))
        p.setPen(QtGui.QPen(rgba(CYAN, 90), 1))
        p.drawLine(QPointF(chart.left(), base), QPointF(chart.right(), base))
        p.setFont(font(8, QtGui.QFont.Weight.DemiBold, 1))
        p.setPen(rgba(DIM))
        p.drawText(QPointF(chart.left(), chart.top() + 8), f"MAX {fmt_hm(vmax)}" if vmax else "KEINE DATEN")

        n = len(self._bars)
        slot = chart.width() / n
        bw = min(34.0, max(4.0, slot * 0.6))  # bei nur 1–2 Jahren keine Riesenbalken
        label_font = font(8, QtGui.QFont.Weight.DemiBold)
        fm = QtGui.QFontMetricsF(label_font)
        widest = max(fm.horizontalAdvance(b.short) for b, _ in self._bars)
        label_every = 1 if widest + 4 <= slot else 2
        for i, (bucket, v) in enumerate(self._bars):
            x = chart.left() + i * slot + (slot - bw) / 2
            last = i == n - 1
            hover = i == self._hover
            color = GREEN if last else CYAN
            if v > 0 and vmax > 0:
                h = max(2.0, v / vmax * span)
                r = QRectF(x, base - h, bw, h)
                if hover or last:
                    p.fillRect(r.adjusted(-3, -3, 3, 0), rgba(color, 40 if hover else 22))
                g = QtGui.QLinearGradient(0, r.top(), 0, r.bottom())
                g.setColorAt(0, rgba(color, 255 if hover else 220))
                g.setColorAt(1, rgba(color, 40))
                p.fillRect(r, g)
                p.fillRect(QRectF(r.left(), r.top(), r.width(), 2), rgba((240, 252, 255) if hover else color))
            else:
                p.fillRect(QRectF(x, base - 1, bw, 1), rgba(color, 70))
            if last or hover or (n - 1 - i) % label_every == 0:
                p.setFont(label_font)
                p.setPen(rgba(TEXT if (hover or last) else DIM))
                p.drawText(QRectF(x - 10, base + 3, bw + 20, 12), Qt.AlignmentFlag.AlignCenter, bucket.short)

    def _paint_footer(self, p: QtGui.QPainter, lay: _Layout) -> None:
        s = self._summary
        if self._hover is not None and self._hover < len(self._bars):
            bucket, v = self._bars[self._hover]
            text, color = f"{bucket.long}   ·   {fmt_hm(v)}", TEXT
        else:
            text = f"SESSIONS {s.sessions}   ·   Ø {fmt_hm(s.average)}   ·   LÄNGSTE {fmt_hm(s.longest)}"
            color = MUTED
        p.setFont(font(9, QtGui.QFont.Weight.DemiBold, 1.2))
        p.setPen(rgba(color))
        p.drawText(QRectF(0, lay.footer_y - 11, W, 16), Qt.AlignmentFlag.AlignCenter, text)

    # --- Maus ---------------------------------------------------------------

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self._press = (e.globalPosition().toPoint(), self.pos())
            self._moved = False

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        if self._press is not None and not self._s.locked:
            start, origin = self._press
            delta = e.globalPosition().toPoint() - start
            if self._moved or delta.manhattanLength() > 4:
                self._moved = True
                self.move(origin + delta)
                return
        hover = self._bar_index_at(e.position()) if self._s.expanded else None
        if hover != self._hover:
            self._hover = hover
            self.update()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() != Qt.MouseButton.LeftButton or self._press is None:
            return
        self._press = None
        if self._moved:
            self._s.x, self._s.y = self.x(), self.y()
            self._save()
            return
        pos = e.position()
        lay = self._layout()
        for ch, r in lay.chips:
            if r.contains(pos):
                self._s.channel = ch
                return self._changed()
        for key, _label, r in lay.tabs:
            if r.contains(pos):
                self._s.tab = key
                return self._changed()
        if pos.y() < H_COMPACT:
            self.set_expanded(not self._s.expanded)

    def leaveEvent(self, _e: QtCore.QEvent) -> None:
        if self._hover is not None:
            self._hover = None
            self.update()

    def contextMenuEvent(self, e: QtGui.QContextMenuEvent) -> None:
        menu = QtWidgets.QMenu(self)
        self.populate_menu(menu)
        menu.exec(e.globalPos())

    # --- Aktionen / Menü ----------------------------------------------------

    def _changed(self) -> None:
        self._save()
        self.refresh()

    def set_expanded(self, on: bool) -> None:
        self._s.expanded = on
        self._hover = None
        self._changed()

    def populate_menu(self, menu: QtWidgets.QMenu, tray: bool = False) -> None:
        s = self._s
        title = menu.addAction(f"SC PLAYTIME  {__version__}")
        title.setEnabled(False)
        if self.updates is not None:
            self.updates.add_install_action(menu)
        if tray:
            menu.addAction("Overlay einblenden" if self._user_hidden else "Overlay ausblenden", self.toggle_hidden)
        self._check(menu, "Statistik aufgeklappt", s.expanded, self.set_expanded)

        games = menu.addMenu("Spiel")
        group = QtGui.QActionGroup(games)
        for g in s.game_list():
            act = games.addAction(f"{g.name}   ({g.exe})")
            act.setCheckable(True)
            act.setChecked(g.name == self._game)
            act.setActionGroup(group)
            act.triggered.connect(lambda _c=False, n=g.name: self._select_game(n))
        games.addSeparator()
        games.addAction("Spiel hinzufügen …", self._add_game)
        if len(s.game_list()) > 1:
            remove = games.addMenu("Spiel entfernen")
            for g in s.game_list():
                act = remove.addAction(g.name)
                act.triggered.connect(lambda _c=False, n=g.name: self._remove_game(n))

        menu.addSeparator()
        menu.addAction(self._slider(menu, "HINTERGRUND", 0, 100, s.bg_alpha, self._set_bg_alpha))
        menu.addAction(self._slider(menu, "DECKKRAFT GESAMT", 20, 100, s.opacity, self._set_opacity))
        colors = menu.addMenu("Farben")
        self._color_menu(colors.addMenu("Statistik-Kacheln (im Spiel)"), "tile", TILE_PRESETS)
        self._color_menu(colors.addMenu("Aktiver Channel"), "chip", CHIP_PRESETS)
        menu.addSeparator()
        self._check(menu, "Position sperren", s.locked, lambda on: self._set("locked", on))
        self._check(menu, "Klicks durchlassen (nur über Tray zurück)", s.click_through, self._set_click_through)
        self._check(menu, "Nur anzeigen, wenn ein Spiel läuft", s.hide_when_offline,
                    lambda on: self._set("hide_when_offline", on))
        self._check(menu, "Mit Windows starten", autostart.is_enabled(), autostart.set_enabled)
        menu.addSeparator()
        menu.addAction("Hilfe …", docs.show_help)
        menu.addAction("Was ist neu? …", docs.show_changelog)
        if self.updates is not None:
            self.updates.populate_menu(menu)
        menu.addSeparator()
        menu.addAction("Datenordner öffnen", lambda: os.startfile(str(data_dir())))
        menu.addAction("Beenden", QtWidgets.QApplication.quit)

    @staticmethod
    def _check(menu: QtWidgets.QMenu, text: str, checked: bool, slot: Callable[[bool], None]) -> None:
        act = menu.addAction(text)
        act.setCheckable(True)
        act.setChecked(checked)
        act.toggled.connect(slot)

    @staticmethod
    def _slider(menu: QtWidgets.QMenu, title: str, lo: int, hi: int, value: int,
                on_change: Callable[[int], None]) -> QtWidgets.QWidgetAction:
        w = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(w)
        lay.setContentsMargins(24, 4, 18, 6)
        lay.setSpacing(4)
        label = QtWidgets.QLabel(f"{title}  {value} %")
        slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        slider.setRange(lo, hi)
        slider.setValue(value)
        slider.setFixedWidth(190)

        def changed(v: int) -> None:
            label.setText(f"{title}  {v} %")
            on_change(v)

        slider.valueChanged.connect(changed)
        lay.addWidget(label)
        lay.addWidget(slider)
        act = QtWidgets.QWidgetAction(menu)
        act.setDefaultWidget(w)
        return act

    def _set(self, name: str, value: object) -> None:
        setattr(self._s, name, value)
        self._changed()

    def _set_bg_alpha(self, v: int) -> None:
        self._s.bg_alpha = v
        self._save()
        self.update()

    def _set_opacity(self, v: int) -> None:
        self._s.opacity = v
        self.setWindowOpacity(v / 100)
        self._save()

    def _color_menu(self, menu: QtWidgets.QMenu, prefix: str,
                    presets: tuple[tuple[str, str, str], ...]) -> None:
        """Vorlagen + freie Farbwahl für Hintergrund/Schrift (Settings <prefix>_bg / <prefix>_fg)."""
        bg_name, fg_name = f"{prefix}_bg", f"{prefix}_fg"
        current = (getattr(self._s, bg_name), getattr(self._s, fg_name))
        group = QtGui.QActionGroup(menu)
        for label, bg, fg in presets:
            act = menu.addAction(label)
            act.setCheckable(True)
            act.setChecked(current == (bg, fg))
            act.setActionGroup(group)
            act.triggered.connect(lambda _c=False, b=bg, f=fg: self._set_colors(bg_name, b, fg_name, f))
        menu.addSeparator()
        menu.addAction("Hintergrundfarbe wählen …", lambda: self._pick_color(bg_name, "Hintergrundfarbe"))
        menu.addAction("Schriftfarbe wählen …", lambda: self._pick_color(fg_name, "Schriftfarbe"))

    def _set_colors(self, bg_name: str, bg: str, fg_name: str, fg: str) -> None:
        setattr(self._s, bg_name, bg)
        self._set(fg_name, fg)

    def _pick_color(self, name: str, title: str) -> None:
        current = getattr(self._s, name)
        start = QtGui.QColor(current) if current else QtGui.QColor("#ffffff" if name.endswith("_fg") else "#0f5132")
        color = QtWidgets.QColorDialog.getColor(start, None, title)
        if color.isValid():
            self._set(name, color.name())

    def _set_click_through(self, on: bool) -> None:
        self._s.click_through = on
        self._apply_flags()
        self._save()

    # --- Spiele verwalten ---------------------------------------------------

    def _select_game(self, name: str) -> None:
        self._s.game = name
        self._s.channel = ""
        self._changed()

    def _add_game(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Spiel-EXE wählen", "", "Programme (*.exe)")
        if not path:
            return
        exe = Path(path).name
        name, ok = QtWidgets.QInputDialog.getText(None, "Spiel hinzufügen", "Anzeigename:", text=Path(path).stem)
        name = name.strip()
        if not ok or not name:
            return
        self._s.games = [g for g in self._s.games if g.get("name") != name] + [{"name": name, "exe": exe}]
        self._s.game = name
        self._s.channel = ""
        self.games_changed.emit()
        self._changed()

    def _remove_game(self, name: str) -> None:
        answer = QtWidgets.QMessageBox.question(
            None, "Spiel entfernen",
            f"»{name}« nicht mehr verfolgen?\nBisherige Sessions bleiben gespeichert.",
        )
        if answer != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        self._s.games = [g for g in self._s.games if g.get("name") != name]
        if self._s.game == name:
            self._s.game = self._s.games[0]["name"]
            self._s.channel = ""
        self.games_changed.emit()
        self._changed()
