"""Export aller Sessions als CSV (für Excel & Co.) oder JSON."""

from __future__ import annotations

import csv
import io
import json
from datetime import datetime
from typing import Sequence

from .store import SessionRow

FIELDS = ("game", "channel", "version", "start", "end", "duration_s", "duration_min")


def _local(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def to_csv(rows: Sequence[SessionRow], delimiter: str = ";") -> str:
    """Eine Zeile je Session, Zeiten in Ortszeit.

    Excel erwartet in Ländern mit Dezimalkomma ``;`` als Trenner, sonst ``,``.
    """
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delimiter, lineterminator="\r\n")
    w.writerow(FIELDS)
    for r in rows:
        seconds = int(round(r.end - r.start))
        w.writerow([r.game, r.channel, r.version, _local(r.start), _local(r.end), seconds, round(seconds / 60)])
    return buf.getvalue()


def to_json(rows: Sequence[SessionRow]) -> str:
    """Zeiten als ISO 8601 mit Zeitzone und zusätzlich als Unix-Zeitstempel."""
    data = [
        {
            "game": r.game,
            "channel": r.channel,
            "version": r.version,
            "start": datetime.fromtimestamp(r.start).astimezone().isoformat(timespec="seconds"),
            "end": datetime.fromtimestamp(r.end).astimezone().isoformat(timespec="seconds"),
            "start_unix": r.start,
            "end_unix": r.end,
            "duration_s": int(round(r.end - r.start)),
        }
        for r in rows
    ]
    return json.dumps({"sessions": data}, indent=2, ensure_ascii=False)
