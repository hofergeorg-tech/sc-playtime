"""Tests zum Security-/Performance-Review (v1.4.1): schnelle Statistik, Update-Prüfsumme, sicheres Speichern."""

import hashlib
import random
import sys
import tempfile
import time
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sc_playtime.settings import Settings  # noqa: E402
from sc_playtime.stats import (STREAK_MIN_S, bucket_totals, buckets, daily_totals, played,  # noqa: E402
                               summarize)
from sc_playtime.store import Store  # noqa: E402
from sc_playtime.tracker import Game, Tracker  # noqa: E402
from sc_playtime.updater import matches_checksum, parse_release  # noqa: E402


def _ts(d: date) -> float:
    return datetime(d.year, d.month, d.day).timestamp()


def old_streak(sessions, today: date) -> int:
    """Die bisherige (quadratische) Berechnung der Serie, als Referenz."""
    day, streak = today, 0
    if played(sessions, _ts(day), _ts(day + timedelta(days=1))) < STREAK_MIN_S:
        day -= timedelta(days=1)
    while played(sessions, _ts(day), _ts(day + timedelta(days=1))) >= STREAK_MIN_S:
        streak += 1
        day -= timedelta(days=1)
    return streak


def random_sessions(n: int, seed: int, days_back: int = 400):
    rnd = random.Random(seed)
    now = datetime(2026, 10, 9, 21).timestamp()
    out = []
    for _ in range(n):
        start = now - rnd.uniform(0, days_back * 86400)
        out.append((start, start + rnd.choice([30, 600, 3600, 4 * 3600, 9 * 3600])))  # teils über Mitternacht
    # eine lückenlose Serie bis heute
    for d in range(25):
        s = now - d * 86400 - 2 * 3600
        out.append((s, s + 1800))
    return sorted(out), datetime.fromtimestamp(now)


class FastStatsTest(unittest.TestCase):
    def test_same_numbers_as_before(self) -> None:
        sessions, now = random_sessions(400, seed=7)
        days = daily_totals(sessions)
        for kind, count in (("day", 14), ("week", 12), ("month", 12), ("year", 5)):
            periods = buckets(kind, now.date(), count)
            for got, b in zip(bucket_totals(days, periods), periods):
                self.assertAlmostEqual(got, played(sessions, b.start, b.end), places=3, msg=f"{kind} {b.long}")
        s = summarize(sessions, now)
        end = now.timestamp()
        self.assertEqual(s.streak, old_streak(sessions, now.date()))
        self.assertAlmostEqual(s.today, played(sessions, _ts(now.date()), end), places=3)
        week_start = now.date() - timedelta(days=now.date().weekday())
        self.assertAlmostEqual(s.week, played(sessions, _ts(week_start), end), places=3)
        self.assertAlmostEqual(s.year, played(sessions, _ts(date(now.year, 1, 1)), end), places=3)

    def test_long_history_stays_fast(self) -> None:
        sessions, now = random_sessions(5000, seed=3, days_back=4 * 365)
        start = time.perf_counter()
        summarize(sessions, now)
        bucket_totals(daily_totals(sessions), buckets("day", now.date(), 14))
        # früher ~1,5 s für die gleiche Menge; großzügige Grenze für langsame CI-Rechner
        self.assertLess(time.perf_counter() - start, 0.5)


class TrackerRevisionTest(unittest.TestCase):
    def test_closed_and_live_are_separate_and_revision_moves_only_on_changes(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            store = Store(Path(d) / "p.db")
            running = {"starcitizen.exe": 1}
            tracker = Tracker(store, [Game("Star Citizen", "StarCitizen.exe")],
                              find=lambda names: dict(running), start_time=lambda pid: 1000.0,
                              image_path=lambda pid: r"C:\SC\LIVE\Bin64\StarCitizen.exe",
                              version=lambda pid: "4.3", idle=lambda: 0.0)
            tracker.poll(now=1100.0)
            rev = tracker.revision
            self.assertEqual(tracker.closed_sessions("Star Citizen"), [])
            self.assertEqual(tracker.live_span("Star Citizen"), (1000.0, 1100.0))
            tracker.poll(now=1200.0)  # nur verlängert
            self.assertEqual(tracker.revision, rev)
            self.assertEqual(tracker.live_span("Star Citizen", "LIVE"), (1000.0, 1200.0))
            self.assertIsNone(tracker.live_span("Star Citizen", "PTU"))
            running.clear()
            tracker.poll(now=1300.0)  # Spiel beendet
            self.assertGreater(tracker.revision, rev)
            self.assertIsNone(tracker.live_span("Star Citizen"))
            self.assertEqual(tracker.closed_sessions("Star Citizen"), [(1000.0, 1300.0)])
            store.close()


class UpdateChecksumTest(unittest.TestCase):
    def test_release_digest_is_read(self) -> None:
        rel = parse_release({"tag_name": "v9.0.0", "assets": [
            {"name": "other.zip", "browser_download_url": "x", "digest": "sha256:00"},
            {"name": "SC-Playtime.exe", "browser_download_url": "https://e/a.exe", "digest": "sha256:ABCDEF"},
            {"name": "SC-Playtime-linux-x86_64", "browser_download_url": "https://e/a", "digest": "sha256:ABCDEF"},
        ]})
        self.assertEqual(rel.version, "9.0.0")
        self.assertEqual(rel.sha256, "abcdef")
        self.assertIsNone(parse_release({"tag_name": "v1", "assets": []}).sha256)

    def test_only_the_exact_file_passes(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "new.exe"
            f.write_bytes(b"abc")
            good = hashlib.sha256(b"abc").hexdigest()
            self.assertTrue(matches_checksum(f, good))
            self.assertTrue(matches_checksum(f, good.upper()))
            self.assertTrue(matches_checksum(f, None))  # alte Releases ohne Prüfsumme
            f.write_bytes(b"abd")
            self.assertFalse(matches_checksum(f, good))


class SettingsSaveTest(unittest.TestCase):
    def test_save_replaces_the_file_in_one_step(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            Settings(game="Elite").save(path)
            Settings(game="Star Citizen", afk_minutes=10).save(path)
            self.assertEqual(Settings.load(path).afk_minutes, 10)
            self.assertEqual([p.name for p in Path(d).iterdir()], ["settings.json"])  # keine .tmp-Reste


if __name__ == "__main__":
    unittest.main()
