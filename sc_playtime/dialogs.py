"""Zusatzfenster: Über (mit Spenden-Knopf), Auswertung, Sessions bearbeiten, Tastenkürzel."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Callable, Optional, Sequence

from PySide6 import QtCore, QtGui, QtWidgets

from . import __version__, docs, hotkeys
from .i18n import tr, tr_list
from .settings import Settings
from .stats import PatchStats, by_version, fmt_hm, heatmap

Qt = QtCore.Qt

WEBSITE = "https://www.georg-hofer.com"
REPOSITORY = "https://github.com/hofergeorg-tech/sc-playtime"
# PayPal-Spendenlink (wie bei NoFences); leer = kein Spenden-Knopf
DONATE_URL = ("https://www.paypal.com/donate/?business=USLSACVSEY8YW&no_recurring=0"
              "&item_name=Coffee+donation&currency_code=EUR")

_open: dict[str, QtWidgets.QWidget] = {}  # Schlüssel → offenes Fenster (je Art nur eins)


def _single(key: str, make: Callable[[], QtWidgets.QWidget]) -> QtWidgets.QWidget:
    """Fenster einmalig öffnen; ist es schon offen, nach vorne holen."""
    win = _open.get(key)
    if win is None or not win.isVisible():
        win = make()
        win.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        win.destroyed.connect(lambda _o=None, k=key: _open.pop(k, None))
        _open[key] = win
    win.show()
    win.raise_()
    win.activateWindow()
    return win


def close_all() -> None:
    """Vor dem Sprachwechsel: offene Fenster schließen, sie zeigen sonst alte Texte."""
    for win in list(_open.values()):
        win.close()


def _date(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime(tr("fmt.date"))


def _datetime(ts: float) -> str:
    return QtCore.QDateTime.fromSecsSinceEpoch(int(ts)).toString(tr("fmt.datetime"))


def _section(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setStyleSheet("color: #5fd0ff; font-weight: 700; letter-spacing: 2px; margin-top: 6px;")
    return label


def _muted(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setWordWrap(True)
    label.setStyleSheet("color: #6f93a8;")
    return label


# --- Über -----------------------------------------------------------------------


def _link(text: str, url: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(f'<a href="{url}" style="color:#5fd0ff; text-decoration:none">{text}</a>')
    label.setOpenExternalLinks(True)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    return label


def open_donate() -> None:
    if DONATE_URL:
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(DONATE_URL))


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, icon: QtGui.QIcon) -> None:
        super().__init__(None)
        self.setWindowTitle(tr("about.title"))
        self.setWindowIcon(icon)
        logo = QtWidgets.QLabel()
        logo.setPixmap(icon.pixmap(64, 64))
        logo.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QtWidgets.QLabel(f"SC Playtime {__version__}")
        f = title.font()
        f.setPointSizeF(f.pointSizeF() * 1.6)
        f.setBold(True)
        title.setFont(f)
        tagline = QtWidgets.QLabel(tr("about.tagline"))
        tagline.setWordWrap(True)

        text = QtWidgets.QVBoxLayout()
        text.setSpacing(4)
        text.addWidget(title)
        text.addWidget(tagline)
        text.addSpacing(10)
        text.addWidget(QtWidgets.QLabel("© 2026 Georg Hofer"))
        text.addWidget(_link("www.georg-hofer.com", WEBSITE))
        text.addWidget(_link(tr("about.source"), REPOSITORY))
        text.addSpacing(10)
        text.addWidget(_muted(tr("about.license")))
        if DONATE_URL:
            text.addSpacing(10)
            hint = QtWidgets.QLabel(tr("about.donate_hint"))
            hint.setWordWrap(True)
            text.addWidget(hint)

        top = QtWidgets.QHBoxLayout()
        top.setSpacing(16)
        top.addWidget(logo)
        top.addLayout(text, 1)

        buttons = QtWidgets.QHBoxLayout()
        if DONATE_URL:
            donate = QtWidgets.QPushButton("♥  " + tr("about.donate"))
            # PayPal-Blau, damit der Knopf auffällt
            donate.setStyleSheet("QPushButton { background: #0070ba; border-color: #2c8fd6; color: #ffffff; "
                                 "font-weight: 700; } QPushButton:hover { background: #1585cf; }")
            donate.clicked.connect(open_donate)
            buttons.addWidget(donate)
        buttons.addStretch(1)
        whats_new = QtWidgets.QPushButton(tr("doc.changelog"))
        whats_new.clicked.connect(docs.show_changelog)
        close = QtWidgets.QPushButton(tr("doc.close"))
        close.setDefault(True)
        close.clicked.connect(self.close)
        buttons.addWidget(whats_new)
        buttons.addWidget(close)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 16)
        lay.addLayout(top)
        lay.addSpacing(14)
        lay.addLayout(buttons)
        self.setFixedWidth(470)


def show_about(icon: QtGui.QIcon) -> None:
    _single("about", lambda: AboutDialog(icon))


# --- Auswertung -----------------------------------------------------------------


class HeatmapWidget(QtWidgets.QWidget):
    """7 Zeilen (Mo–So) × 24 Spalten (Stunden), je heller desto mehr gespielt."""

    LEFT, TOP, CELL_H = 40, 18, 22

    def __init__(self, grid: list[list[float]]) -> None:
        super().__init__()
        self._grid = grid
        self._max = max((v for row in grid for v in row), default=0.0)
        self.setMouseTracking(True)
        self.setMinimumSize(self.LEFT + 24 * 18, self.TOP + 7 * self.CELL_H + 4)

    def _cell(self) -> float:
        return (self.width() - self.LEFT) / 24

    def _at(self, pos: QtCore.QPointF) -> Optional[tuple[int, int]]:
        col = int((pos.x() - self.LEFT) // self._cell())
        row = int((pos.y() - self.TOP) // self.CELL_H)
        return (row, col) if 0 <= row < 7 and 0 <= col < 24 and pos.x() >= self.LEFT else None

    def paintEvent(self, _e: QtGui.QPaintEvent) -> None:
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        cw = self._cell()
        small = QtGui.QFont(self.font())
        small.setPixelSize(10)
        p.setFont(small)
        p.setPen(QtGui.QColor("#6f93a8"))
        for h in range(0, 24, 3):
            p.drawText(QtCore.QRectF(self.LEFT + h * cw, 0, cw * 3, self.TOP - 4),
                       Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom, f"{h:02d}")
        for r, day in enumerate(tr_list("weekdays")):
            y = self.TOP + r * self.CELL_H
            p.setPen(QtGui.QColor("#6f93a8"))
            p.drawText(QtCore.QRectF(0, y, self.LEFT - 8, self.CELL_H),
                       Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, day)
            for h in range(24):
                v = self._grid[r][h]
                cell = QtCore.QRectF(self.LEFT + h * cw + 1, y + 1, cw - 2, self.CELL_H - 2)
                if v > 0 and self._max > 0:
                    # Wurzel, damit auch seltene Stunden sichtbar bleiben
                    k = (v / self._max) ** 0.5
                    p.fillRect(cell, QtGui.QColor(95, 208, 255, int(40 + 215 * k)))
                else:
                    p.fillRect(cell, QtGui.QColor(95, 208, 255, 14))
        p.end()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        hit = self._at(e.position())
        if hit is None:
            QtWidgets.QToolTip.hideText()
            return
        r, h = hit
        text = f"{tr_list('weekdays')[r]} {h:02d}:00–{(h + 1) % 24:02d}:00   {fmt_hm(self._grid[r][h])}"
        QtWidgets.QToolTip.showText(e.globalPosition().toPoint(), text, self)


_ENDING_COLORS = {"crash": "#ff6e6e", "server": "#ffc45a"}  # Marken im Zeitstrahl
_ENDING_TEXT = {"crash": "#d63c3c", "server": "#b87800"}  # Schrift in Tabellen (auf hellem Grund lesbar)


def ending_text(reason: str) -> str:
    return tr(f"end.{reason}") if reason in ("quit", "crash", "server") else ""


def day_segments(rows: Sequence, day: date) -> list[tuple[float, float, object]]:
    """Teile der Sessions, die auf ``day`` fallen, als (Startstunde, Endstunde, Session) – 0…24."""
    start = datetime.combine(day, datetime.min.time()).timestamp()
    end = datetime.combine(day + timedelta(days=1), datetime.min.time()).timestamp()
    length = end - start  # 23/25 h an Tagen der Zeitumstellung
    return [(max(0.0, (r.start - start) / length * 24), min(24.0, (r.end - start) / length * 24), r)
            for r in rows if r.end > start and r.start < end]


def play_days(rows: Sequence) -> list[date]:
    """Alle Tage mit Spielzeit, aufsteigend (Sessions über Mitternacht zählen für beide Tage)."""
    days: set[date] = set()
    for r in rows:
        d = datetime.fromtimestamp(r.start).date()
        last = datetime.fromtimestamp(max(r.start, r.end - 1)).date()
        while d <= last:
            days.add(d)
            d += timedelta(days=1)
    return sorted(days)


class TimelineWidget(QtWidgets.QWidget):
    """Ein Tag als Zeitstrahl 0–24 Uhr: Sessions als Balken in Channel-Farbe, Lücken = Pausen/AFK,
    am Ende eine rote (Absturz) bzw. gelbe (Server-Abbruch) Marke."""

    LEFT, TOP, BAR_H = 8, 18, 26

    def __init__(self) -> None:
        super().__init__()
        self._segments: list[tuple[float, float, object]] = []
        self.setMouseTracking(True)
        self.setMinimumHeight(self.TOP + self.BAR_H + 6)

    def set_day(self, rows: Sequence, day: date) -> None:
        self._segments = day_segments(rows, day)
        self.update()

    def _x(self, hour: float) -> float:
        return self.LEFT + hour / 24 * (self.width() - 2 * self.LEFT)

    def paintEvent(self, _e: QtGui.QPaintEvent) -> None:
        from .ui import CHANNEL_COLORS, CYAN  # ui importiert dialogs – erst hier laden

        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        small = QtGui.QFont(self.font())
        small.setPixelSize(10)
        p.setFont(small)
        track = QtCore.QRectF(self._x(0), self.TOP, self._x(24) - self._x(0), self.BAR_H)
        p.fillRect(track, QtGui.QColor(95, 208, 255, 14))
        for h in range(0, 25, 3):
            x = self._x(h)
            p.setPen(QtGui.QColor(95, 208, 255, 40))
            p.drawLine(QtCore.QPointF(x, self.TOP), QtCore.QPointF(x, self.TOP + self.BAR_H))
            p.setPen(QtGui.QColor("#6f93a8"))
            p.drawText(QtCore.QRectF(x - 20, 0, 40, self.TOP - 4),
                       Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom, f"{h:02d}")
        for a, b, r in self._segments:
            c = CHANNEL_COLORS.get(r.channel, CYAN)
            rect = QtCore.QRectF(self._x(a), self.TOP + 3, max(2.0, self._x(b) - self._x(a)), self.BAR_H - 6)
            p.fillRect(rect, QtGui.QColor(c[0], c[1], c[2], 200))
            # Marke nur, wenn die Session an diesem Tag endet (nicht erst nach Mitternacht)
            if r.reason in _ENDING_COLORS and b < 24:
                p.fillRect(QtCore.QRectF(rect.right() - 3, self.TOP, 4, self.BAR_H), QtGui.QColor(_ENDING_COLORS[r.reason]))
        p.end()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        x = e.position().x()
        hit = next((r for a, b, r in self._segments if self._x(a) - 2 <= x <= self._x(b) + 2), None)
        if hit is None:
            QtWidgets.QToolTip.hideText()
            return
        parts = [f"{_clock(hit.start)}–{_clock(hit.end)}", fmt_hm(hit.end - hit.start), hit.channel, hit.version,
                 ending_text(hit.reason)]
        QtWidgets.QToolTip.showText(e.globalPosition().toPoint(), "  ·  ".join(p for p in parts if p), self)


def _clock(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%H:%M")


def peak_text(grid: list[list[float]]) -> str:
    """Meistgespielter Wochentag und meistgespielte Stunde."""
    days = [sum(row) for row in grid]
    hours = [sum(grid[d][h] for d in range(7)) for h in range(24)]
    if not any(days):
        return tr("hud.no_data")
    d = days.index(max(days))
    h = hours.index(max(hours))
    return tr("stats.peak", when=f"{tr_list('weekdays')[d]}, {h:02d}:00–{(h + 1) % 24:02d}:00")


class StatsDialog(QtWidgets.QDialog):
    def __init__(self, game: str, channel: str, sessions: Sequence[tuple[float, float]],
                 versioned: Sequence[tuple], icon: QtGui.QIcon, rows: Sequence = ()) -> None:
        super().__init__(None, Qt.WindowType.Window)
        self.setWindowTitle(tr("stats.title", game=game))
        self.setWindowIcon(icon)
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(18, 14, 18, 14)
        lay.addWidget(_muted(tr("stats.scope", game=game.upper(), channel=channel or tr("hud.all"))))

        grid = heatmap(sessions)
        lay.addWidget(_section(tr("stats.heatmap")))
        lay.addWidget(_muted(tr("stats.heatmap_hint")))
        lay.addWidget(HeatmapWidget(grid))
        lay.addWidget(QtWidgets.QLabel(peak_text(grid)))

        # Tagesverlauf: ein Tag als Zeitstrahl, blättern zwischen Tagen mit Spielzeit
        self._rows = list(rows)
        self._days = play_days(self._rows)
        lay.addWidget(_section(tr("stats.timeline")))
        nav = QtWidgets.QHBoxLayout()
        self._prev = QtWidgets.QPushButton("‹")
        self._next = QtWidgets.QPushButton("›")
        for b in (self._prev, self._next):
            b.setFixedWidth(32)
        self._prev.clicked.connect(lambda: self._step(-1))
        self._next.clicked.connect(lambda: self._step(1))
        self._day_label = QtWidgets.QLabel()
        self._day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav.addWidget(self._prev)
        nav.addWidget(self._day_label, 1)
        nav.addWidget(self._next)
        lay.addLayout(nav)
        self._timeline = TimelineWidget()
        lay.addWidget(self._timeline)
        self._day_index = len(self._days) - 1  # zuletzt gespielter Tag
        self._show_day()

        lay.addWidget(_section(tr("stats.patches")))
        patches = by_version(versioned)
        if not any(p.version for p in patches):
            lay.addWidget(_muted(tr("stats.no_patch")))
        if patches:
            lay.addWidget(self._patch_table(patches), 1)
            lay.addWidget(_muted(tr("stats.endings_hint")))
        close = QtWidgets.QPushButton(tr("doc.close"))
        close.clicked.connect(self.close)
        lay.addWidget(close, alignment=Qt.AlignmentFlag.AlignRight)
        self.resize(700, 700)

    def _step(self, delta: int) -> None:
        self._day_index = max(0, min(len(self._days) - 1, self._day_index + delta))
        self._show_day()

    def _show_day(self) -> None:
        if not self._days:
            self._day_label.setText(tr("hud.no_data"))
            self._prev.setEnabled(False)
            self._next.setEnabled(False)
            return
        day = self._days[self._day_index]
        segments = day_segments(self._rows, day)
        played = sum((b - a) * 3600 for a, b, _ in segments)
        weekday = tr_list("weekdays")[day.weekday()]
        self._day_label.setText(tr("stats.timeline_day", day=f"{weekday} {day.strftime(tr('fmt.date'))}",
                                   total=fmt_hm(played), count=len(segments)))
        self._prev.setEnabled(self._day_index > 0)
        self._next.setEnabled(self._day_index < len(self._days) - 1)
        self._timeline.set_day(self._rows, day)

    @staticmethod
    def _patch_table(patches: list[PatchStats]) -> QtWidgets.QTableWidget:
        heads = [tr("stats.col_patch"), tr("stats.col_time"), tr("stats.col_sessions"), tr("stats.col_crashes"),
                 tr("stats.col_server"), tr("stats.col_period")]
        table = QtWidgets.QTableWidget(len(patches), len(heads))
        table.setHorizontalHeaderLabels(heads)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        total = sum(p.total for p in patches) or 1.0
        for row, p in enumerate(patches):
            per_crash = p.hours_per_crash()
            crashes = (tr("stats.crash_rate", count=p.crashes, every=fmt_hm(per_crash * 3600))
                       if per_crash is not None else "0")
            cells = (p.version or tr("stats.unknown"), f"{fmt_hm(p.total)}  ({p.total / total:.0%})",
                     str(p.sessions), crashes, str(p.server), f"{_date(p.first)} – {_date(p.last)}")
            for col, text in enumerate(cells):
                item = QtWidgets.QTableWidgetItem(text)
                if col in (1, 2, 3, 4):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                if col == 3 and p.crashes:
                    item.setForeground(QtGui.QColor(_ENDING_TEXT["crash"]))
                if col == 4 and p.server:
                    item.setForeground(QtGui.QColor(_ENDING_TEXT["server"]))
                table.setItem(row, col, item)
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        return table


def show_stats(game: str, channel: str, sessions: Sequence[tuple[float, float]],
               versioned: Sequence[tuple], icon: QtGui.QIcon, rows: Sequence = ()) -> None:
    # bei erneutem Aufruf neu aufbauen, die Daten könnten sich geändert haben
    old = _open.get("stats")
    if old is not None:
        old.close()
    _single("stats", lambda: StatsDialog(game, channel, sessions, versioned, icon, rows))


# --- Sessions bearbeiten --------------------------------------------------------


class EditSessionDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, start: float, end: float) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("sess.edit_title"))
        self._start = self._edit(start)
        self._end = self._edit(end)
        form = QtWidgets.QFormLayout()
        form.addRow(tr("sess.start"), self._start)
        form.addRow(tr("sess.end"), self._end)
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._accept)
        buttons.rejected.connect(self.reject)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addLayout(form)
        lay.addWidget(buttons)

    @staticmethod
    def _edit(ts: float) -> QtWidgets.QDateTimeEdit:
        edit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.fromSecsSinceEpoch(int(ts)))
        edit.setDisplayFormat(tr("fmt.datetime"))
        edit.setCalendarPopup(True)
        return edit

    def values(self) -> tuple[float, float]:
        return float(self._start.dateTime().toSecsSinceEpoch()), float(self._end.dateTime().toSecsSinceEpoch())

    def _accept(self) -> None:
        start, end = self.values()
        if end <= start:
            QtWidgets.QMessageBox.warning(self, tr("sess.edit_title"), tr("sess.invalid"))
            return
        self.accept()


class SessionsDialog(QtWidgets.QDialog):
    def __init__(self, tracker, game: str, on_change: Callable[[], None], icon: QtGui.QIcon) -> None:
        super().__init__(None, Qt.WindowType.Window)
        self._tracker = tracker
        self._game = game
        self._on_change = on_change
        self.setWindowTitle(tr("sess.title", game=game))
        self.setWindowIcon(icon)
        heads = [tr("sess.col_start"), tr("sess.col_end"), tr("sess.col_duration"),
                 tr("sess.col_channel"), tr("sess.col_patch"), tr("sess.col_ending")]
        self._table = QtWidgets.QTableWidget(0, len(heads))
        self._table.setHorizontalHeaderLabels(heads)
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self._table.itemSelectionChanged.connect(self._update_buttons)
        self._table.doubleClicked.connect(lambda _i: self._edit())

        self._edit_btn = QtWidgets.QPushButton(tr("sess.edit"))
        self._edit_btn.clicked.connect(self._edit)
        self._delete_btn = QtWidgets.QPushButton(tr("sess.delete"))
        self._delete_btn.clicked.connect(self._delete)
        close = QtWidgets.QPushButton(tr("doc.close"))
        close.clicked.connect(self.close)
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(self._edit_btn)
        buttons.addWidget(self._delete_btn)
        buttons.addStretch(1)
        buttons.addWidget(close)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self._table, 1)
        lay.addWidget(_muted(tr("sess.hint")))
        lay.addLayout(buttons)
        self.resize(640, 520)
        self._load()

    def _load(self) -> None:
        rows = list(reversed(self._tracker.rows(self._game)))  # neueste oben
        self._table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            live = self._tracker.is_live(r.id)
            cells = (_datetime(r.start), tr("sess.running") if live else _datetime(r.end),
                     fmt_hm(r.end - r.start), r.channel, r.version, ending_text(r.reason))
            for col, text in enumerate(cells):
                item = QtWidgets.QTableWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, r.id)
                if live:
                    item.setForeground(QtGui.QColor("#64ffb4"))
                elif col == 5 and r.reason in _ENDING_TEXT:
                    item.setForeground(QtGui.QColor(_ENDING_TEXT[r.reason]))
                self._table.setItem(i, col, item)
        self._table.resizeColumnsToContents()
        self._table.horizontalHeader().setStretchLastSection(True)
        self._update_buttons()

    def _selected(self) -> list[int]:
        ids = {self._table.item(idx.row(), 0).data(Qt.ItemDataRole.UserRole)
               for idx in self._table.selectionModel().selectedRows()}
        return [i for i in ids if not self._tracker.is_live(i)]

    def _update_buttons(self) -> None:
        sel = self._selected()
        self._edit_btn.setEnabled(len(sel) == 1)
        self._delete_btn.setEnabled(bool(sel))

    def _edit(self) -> None:
        sel = self._selected()
        if len(sel) != 1:
            return
        row = next(r for r in self._tracker.rows(self._game) if r.id == sel[0])
        dlg = EditSessionDialog(self, row.start, row.end)
        if dlg.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        self._tracker.update_session(row.id, *dlg.values())
        self._changed()

    def _delete(self) -> None:
        sel = self._selected()
        if not sel:
            return
        answer = QtWidgets.QMessageBox.question(self, tr("sess.delete"), tr("sess.delete_confirm", count=len(sel)))
        if answer != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        for sid in sel:
            self._tracker.delete_session(sid)
        self._changed()

    def _changed(self) -> None:
        self._load()
        self._on_change()


def show_sessions(tracker, game: str, on_change: Callable[[], None], icon: QtGui.QIcon) -> None:
    old = _open.get("sessions")
    if old is not None and getattr(old, "_game", None) != game:
        old.close()
    _single("sessions", lambda: SessionsDialog(tracker, game, on_change, icon))


# --- Tastenkürzel ---------------------------------------------------------------


class HotkeyDialog(QtWidgets.QDialog):
    def __init__(self, settings: Settings) -> None:
        super().__init__(None)
        self.setWindowTitle(tr("hk.title"))
        self._toggle = self._edit(settings.hotkey_toggle)
        self._click = self._edit(settings.hotkey_click)
        self._anti_afk = self._edit(settings.hotkey_anti_afk)
        form = QtWidgets.QFormLayout()
        form.addRow(tr("hk.toggle"), self._toggle)
        form.addRow(tr("hk.click"), self._click)
        form.addRow(tr("hk.anti_afk"), self._anti_afk)
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(_muted(tr("hk.hint") if hotkeys.SUPPORTED else tr("hk.unsupported")))
        lay.addLayout(form)
        lay.addWidget(buttons)
        self.setMinimumWidth(440)

    @staticmethod
    def _edit(text: str) -> QtWidgets.QKeySequenceEdit:
        edit = QtWidgets.QKeySequenceEdit(QtGui.QKeySequence(text))
        edit.setMaximumSequenceLength(1)
        edit.setClearButtonEnabled(True)
        return edit

    def values(self) -> tuple[str, str, str]:
        fmt = QtGui.QKeySequence.SequenceFormat.PortableText
        return tuple(e.keySequence().toString(fmt) for e in (self._toggle, self._click, self._anti_afk))
