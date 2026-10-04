"""Auswertung: Sessions auf Tage/Wochen/Monate/Jahre verteilen.

Sessions über Mitternacht (oder Wochen-/Monatsgrenzen) werden anteilig
aufgeteilt — gezählt wird immer nur die Überlappung mit dem Zeitraum.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Sequence

from .i18n import tr, tr_list

Session = tuple[float, float]

BUCKET_COUNT = {"day": 14, "week": 12, "month": 12, "year": 5}
# Tage mit weniger Spielzeit zählen nicht zur Serie (kurz Launcher-Test o. ä.)
STREAK_MIN_S = 60.0


def _ts(d: date) -> float:
    return datetime(d.year, d.month, d.day).timestamp()


def _add_months(year: int, month: int, delta: int) -> tuple[int, int]:
    idx = year * 12 + (month - 1) + delta
    return idx // 12, idx % 12 + 1


def played(sessions: Sequence[Session], start: float, end: float) -> float:
    return sum(max(0.0, min(e, end) - max(s, start)) for s, e in sessions)


@dataclass(frozen=True)
class Bucket:
    short: str  # Achsenbeschriftung
    long: str  # Hover-Text
    start: float
    end: float


def buckets(kind: str, today: date, n: int, offset: int = 0) -> list[Bucket]:
    """``n`` Zeiträume der Art ``kind``, ältester zuerst.

    ``offset`` verschiebt das Fenster um so viele Zeiträume in die Vergangenheit
    (0 = der letzte Balken ist der laufende Zeitraum).
    """
    out: list[Bucket] = []
    weekdays, months = tr_list("weekdays"), tr_list("months")
    fmt_date, fmt_short = tr("fmt.date"), tr("fmt.date_short")
    for i in range(n - 1 + offset, offset - 1, -1):
        if kind == "day":
            d = today - timedelta(days=i)
            nxt = d + timedelta(days=1)
            out.append(Bucket(str(d.day), f"{weekdays[d.weekday()]} {d.strftime(fmt_date)}", _ts(d), _ts(nxt)))
        elif kind == "week":
            mon = today - timedelta(days=today.weekday(), weeks=i)
            sun = mon + timedelta(days=6)
            kw = mon.isocalendar()[1]
            long = tr("week.long", week=kw, start=mon.strftime(fmt_short), end=sun.strftime(fmt_date))
            out.append(Bucket(str(kw), long, _ts(mon), _ts(sun + timedelta(days=1))))
        elif kind == "month":
            y, m = _add_months(today.year, today.month, -i)
            y2, m2 = _add_months(y, m, 1)
            out.append(Bucket(months[m - 1], f"{months[m - 1]} {y}", _ts(date(y, m, 1)), _ts(date(y2, m2, 1))))
        elif kind == "year":
            y = today.year - i
            out.append(Bucket(str(y), str(y), _ts(date(y, 1, 1)), _ts(date(y + 1, 1, 1))))
        else:
            raise ValueError(f"unbekannter Zeitraum: {kind}")
    return out


def periods_back(kind: str, first: date, today: date) -> int:
    """Wie viele Zeiträume ``first`` vor dem laufenden liegt (0 = derselbe)."""
    if kind == "day":
        return max(0, (today - first).days)
    if kind == "week":
        monday = lambda d: d - timedelta(days=d.weekday())  # noqa: E731
        return max(0, (monday(today) - monday(first)).days // 7)
    if kind == "month":
        return max(0, (today.year - first.year) * 12 + today.month - first.month)
    if kind == "year":
        return max(0, today.year - first.year)
    raise ValueError(f"unbekannter Zeitraum: {kind}")


def max_offset(kind: str, first: date, today: date, n: int) -> int:
    """Weitestes Zurückblättern: bis der älteste Balken die erste Session zeigt."""
    return max(0, periods_back(kind, first, today) - (n - 1))


def heatmap(sessions: Sequence[Session]) -> list[list[float]]:
    """Spielzeit je Wochentag (0 = Montag) und Stunde: ``grid[weekday][hour]`` in Sekunden."""
    grid = [[0.0] * 24 for _ in range(7)]
    for s, e in sessions:
        t = s
        while t < e:
            dt = datetime.fromtimestamp(t)
            nxt = (dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)).timestamp()
            if nxt <= t:  # Zeitumstellung: Stunde ohne Fortschritt überspringen
                nxt = t + 3600
            grid[dt.weekday()][dt.hour] += min(e, nxt) - t
            t = nxt
    return grid


@dataclass(frozen=True)
class PatchStats:
    version: str  # "" = unbekannt (Sessions vor 1.4 oder kein Star Citizen)
    total: float
    sessions: int
    first: float
    last: float


def _version_key(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v.split(".") if p.isdigit())


def by_version(rows: Sequence[tuple[str, float, float]]) -> list[PatchStats]:
    """Spielzeit je Patch, neuester zuerst; Unbekanntes ans Ende."""
    groups: dict[str, list[tuple[float, float]]] = {}
    for version, s, e in rows:
        groups.setdefault(version, []).append((s, e))
    out = [
        PatchStats(v, sum(e - s for s, e in ss), sum(1 for s, e in ss if e - s >= STREAK_MIN_S),
                   min(s for s, _ in ss), max(e for _, e in ss))
        for v, ss in groups.items()
    ]
    return sorted(out, key=lambda p: (p.version != "", _version_key(p.version)), reverse=True)


@dataclass(frozen=True)
class Summary:
    today: float
    week: float
    month: float
    year: float
    total: float
    sessions: int
    average: float
    longest: float
    streak: int


def summarize(sessions: Sequence[Session], now: datetime) -> Summary:
    today = now.date()
    end = now.timestamp()

    def since(d: date) -> float:
        return played(sessions, _ts(d), end)

    durations = [e - s for s, e in sessions if e - s >= STREAK_MIN_S]

    streak = 0
    day = today
    if played(sessions, _ts(day), _ts(day + timedelta(days=1))) < STREAK_MIN_S:
        day -= timedelta(days=1)  # heute noch nicht gespielt bricht die Serie nicht
    while played(sessions, _ts(day), _ts(day + timedelta(days=1))) >= STREAK_MIN_S:
        streak += 1
        day -= timedelta(days=1)

    return Summary(
        today=since(today),
        week=since(today - timedelta(days=today.weekday())),
        month=since(today.replace(day=1)),
        year=since(date(today.year, 1, 1)),
        total=sum(e - s for s, e in sessions),
        sessions=len(durations),
        average=sum(durations) / len(durations) if durations else 0.0,
        longest=max(durations, default=0.0),
        streak=streak,
    )


def fmt_hm(sec: float) -> str:
    h, m = divmod(int(sec // 60), 60)
    if h == 0:
        return f"{m}m"
    if h >= 100:
        return f"{h}h"
    return f"{h}h {m:02d}m"


def fmt_clock(sec: float) -> str:
    h, rest = divmod(int(sec), 3600)
    m, s = divmod(rest, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
