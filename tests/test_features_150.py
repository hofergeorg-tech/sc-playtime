"""Tests für 1.5.0: Absturz-Erkennung, Tages-Zeitleiste, Zusammenführen mit einem anderen PC."""

import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sc_playtime import endings, merge  # noqa: E402
from sc_playtime.dialogs import day_segments, play_days  # noqa: E402
from sc_playtime.stats import by_version  # noqa: E402
from sc_playtime.store import SessionRow, Store  # noqa: E402
from sc_playtime.tracker import Game, Tracker  # noqa: E402

# Echte Zeilen aus Star-Citizen-Logs (gekürzt)
QUIT_LOG = """<2026-10-09T05:53:31.155Z> CGame::OnDisconnected Client quitting game
<2026-10-09T05:53:31.155Z> [Notice] <SystemQuit> CSystem::Quit invoked with - cause=30016, reason=Quit via console command, exitCode=0, thread id=2208
<2026-10-09T05:53:31.155Z> System Fast Shutdown (ExitOnQuit enabled)
<2026-10-09T05:53:31.156Z> [CIG] CCIGBroker::FastShutdown
"""
CLOSED_LOG = QUIT_LOG.replace("Quit via console command", "User closed the application")
SERVER_LOG = QUIT_LOG.replace("Quit via console command", "Back-end services are unresponsive")
CRASH_LOG = """<2026-10-01T19:45:10.000Z> [Notice] <Something> regular line
Copying game.log...
Copied Game.log to C:\\Users\\x\\AppData\\Local\\Star Citizen\\Crashes\\game.log
All crash related data successfully handed over to crash info collector process
"""


def ts(*a: int) -> float:
    return datetime(*a).timestamp()


class EndingTest(unittest.TestCase):
    def test_reasons_from_real_log_lines(self) -> None:
        self.assertEqual(endings.reason_from_log(QUIT_LOG), endings.QUIT)
        self.assertEqual(endings.reason_from_log(CLOSED_LOG), endings.QUIT)
        self.assertEqual(endings.reason_from_log(SERVER_LOG), endings.SERVER)
        self.assertEqual(endings.reason_from_log(CRASH_LOG), endings.CRASH)
        self.assertEqual(endings.reason_from_log("<x> still loading …"), "")
        # Absturz erst nach dem Quit (beim Herunterfahren) zählt als Absturz
        self.assertEqual(endings.reason_from_log(QUIT_LOG + CRASH_LOG), endings.CRASH)

    def test_backfill_matches_logs_to_sessions_by_end_time(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            live = Path(d) / "LIVE"
            (live / "logbackups").mkdir(parents=True)
            crash = live / "logbackups" / "Game Build(1) 01 Oct 26 (20 05 18).log"
            crash.write_text(CRASH_LOG, encoding="utf-8")
            os.utime(crash, (ts(2026, 10, 1, 21, 45, 30),) * 2)
            server = live / "logbackups" / "Game Build(1) 05 Oct 26 (21 51 04).log"
            server.write_text(SERVER_LOG, encoding="utf-8")
            os.utime(server, (ts(2026, 10, 5, 21, 52),) * 2)
            rows = [
                SessionRow(1, "Star Citizen", "LIVE", ts(2026, 10, 1, 20, 5), ts(2026, 10, 1, 21, 45)),
                SessionRow(2, "Star Citizen", "LIVE", ts(2026, 10, 5, 21, 51), ts(2026, 10, 5, 21, 52, 2)),
                SessionRow(3, "Star Citizen", "PTU", ts(2026, 10, 5, 21, 0), ts(2026, 10, 5, 21, 52)),  # anderer Channel
                SessionRow(4, "Star Citizen", "LIVE", ts(2026, 10, 3, 18, 0), ts(2026, 10, 3, 19, 0)),  # kein Log
                SessionRow(5, "Star Citizen", "LIVE", ts(2026, 10, 1, 20, 0), ts(2026, 10, 1, 21, 45, 10),
                           reason="quit"),  # schon bekannt
            ]
            self.assertEqual(sorted(endings.backfill(rows, [live])), [(1, "crash"), (2, "server")])

    def test_tracker_records_how_the_game_ended(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            store = Store(Path(d) / "p.db")
            running = {"starcitizen.exe": 7}
            seen_dirs = []
            tracker = Tracker(store, [Game("Star Citizen", "StarCitizen.exe")],
                              find=lambda names: dict(running), start_time=lambda pid: 1000.0,
                              image_path=lambda pid: r"C:\SC\LIVE\Bin64\StarCitizen.exe",
                              version=lambda pid: "4.3.1", idle=lambda: 0.0,
                              game_dir=lambda image: Path(d), ending=lambda folder, since: "crash",
                              on_dir=seen_dirs.append)
            tracker.poll(now=1100.0)
            self.assertEqual(seen_dirs, [Path(d)])
            running.clear()
            tracker.poll(now=1200.0)
            self.assertEqual([r.reason for r in store.all()], ["crash"])
            self.assertEqual(tracker.versioned("Star Citizen"), [("4.3.1", 1000.0, 1200.0, "crash")])
            store.close()

    def test_patch_table_counts_crashes_and_disconnects(self) -> None:
        stats = by_version([("4.3.1", 0, 7200, "crash"), ("4.3.1", 8000, 15200, "quit"),
                            ("4.3.1", 16000, 16100, "server"), ("4.3.0", 0, 3600)])
        newest = stats[0]
        self.assertEqual((newest.version, newest.crashes, newest.server), ("4.3.1", 1, 1))
        self.assertAlmostEqual(newest.hours_per_crash(), (7200 + 7200 + 100) / 3600)
        self.assertIsNone(stats[1].hours_per_crash())


class TimelineTest(unittest.TestCase):
    def test_day_segments_clip_at_midnight(self) -> None:
        rows = [SessionRow(1, "SC", "LIVE", ts(2026, 10, 1, 22), ts(2026, 10, 2, 1, 30)),
                SessionRow(2, "SC", "PTU", ts(2026, 10, 2, 18), ts(2026, 10, 2, 19, 30))]
        segs = day_segments(rows, date(2026, 10, 2))
        self.assertEqual([(round(a, 2), round(b, 2), r.id) for a, b, r in segs], [(0.0, 1.5, 1), (18.0, 19.5, 2)])
        self.assertEqual(play_days(rows), [date(2026, 10, 1), date(2026, 10, 2)])


class MergeTest(unittest.TestCase):
    def test_old_database_without_new_columns_can_be_read(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "old.db"
            db = sqlite3.connect(path)
            db.execute("CREATE TABLE sessions (id INTEGER PRIMARY KEY, game TEXT, channel TEXT, start REAL, end REAL)")
            db.execute("INSERT INTO sessions(game, channel, start, end) VALUES ('Star Citizen', 'LIVE', 10, 20)")
            db.commit()
            db.close()
            self.assertEqual(merge.read_sessions(path), [SessionRow(0, "Star Citizen", "LIVE", 10.0, 20.0, "", "")])

    def test_overlapping_sessions_of_the_same_game_are_skipped(self) -> None:
        mine = [SessionRow(1, "Star Citizen", "LIVE", 1000, 2000)]
        theirs = [
            SessionRow(0, "Star Citizen", "LIVE", 1500, 2500),  # überschneidet sich → doppelt
            SessionRow(0, "Star Citizen", "LIVE", 3000, 4000),  # neu
            SessionRow(0, "Star Citizen", "LIVE", 3000, 4000),  # in der Datei doppelt
            SessionRow(0, "Elite", "", 1500, 2500),  # anderes Spiel, gleiche Zeit → neu
        ]
        plan = merge.plan(mine, theirs)
        self.assertEqual([(r.game, r.start) for r in plan.new], [("Star Citizen", 3000), ("Elite", 1500)])
        self.assertEqual(plan.duplicates, 2)
        self.assertEqual(plan.games(), ["Elite", "Star Citizen"])

    def test_merging_twice_adds_nothing_new(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            other = Store(Path(d) / "other.db")
            other.insert([SessionRow(0, "Star Citizen", "PTU", 5000, 6000, "4.4.0", "crash")])
            other.close()
            store = Store(Path(d) / "mine.db")
            tracker = Tracker(store, [], find=lambda names: {})
            plan = merge.plan(tracker.rows(), merge.read_sessions(Path(d) / "other.db"))
            store.insert(plan.new)
            tracker.reload()
            self.assertEqual([(r.channel, r.version, r.reason) for r in tracker.rows()], [("PTU", "4.4.0", "crash")])
            again = merge.plan(tracker.rows(), merge.read_sessions(Path(d) / "other.db"))
            self.assertEqual((again.new, again.duplicates), ([], 1))
            store.close()


class DocsTest(unittest.TestCase):
    def test_every_language_has_help_and_a_changelog_with_this_version(self) -> None:
        from sc_playtime import __version__, i18n

        root = Path(__file__).resolve().parent.parent
        for code in i18n.LANGUAGES:
            files = i18n.DOCS[code]
            help_text = (root / files["help"]).read_text(encoding="utf-8")
            changelog = (root / files["changelog"]).read_text(encoding="utf-8")
            self.assertIn("## ", help_text, code)
            self.assertIn(f"## [{__version__}]", changelog, code)


if __name__ == "__main__":
    unittest.main()
