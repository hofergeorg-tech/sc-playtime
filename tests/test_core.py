import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sc_playtime.process import channel_from_path  # noqa: E402
from sc_playtime.stats import buckets, fmt_clock, fmt_hm, played, summarize  # noqa: E402
from sc_playtime.store import Store  # noqa: E402
from sc_playtime.tracker import Game, Tracker, sort_channels  # noqa: E402


def ts(*a: int) -> float:
    return datetime(*a).timestamp()


class StatsTest(unittest.TestCase):
    def test_session_over_midnight_is_split(self) -> None:
        sessions = [(ts(2026, 9, 27, 23, 0), ts(2026, 9, 28, 1, 30))]
        days = buckets("day", date(2026, 9, 28), 2)
        self.assertEqual([played(sessions, b.start, b.end) for b in days], [3600, 5400])

    def test_summary_periods_and_streak(self) -> None:
        sessions = [
            (ts(2025, 12, 31, 20), ts(2025, 12, 31, 22)),  # Vorjahr
            (ts(2026, 9, 1, 10), ts(2026, 9, 1, 11)),  # diesen Monat, alte Woche
            (ts(2026, 9, 26, 20), ts(2026, 9, 26, 21)),  # Sa
            (ts(2026, 9, 27, 20), ts(2026, 9, 27, 22)),  # So
            (ts(2026, 9, 28, 18), ts(2026, 9, 28, 18, 30)),  # Mo (heute)
        ]
        s = summarize(sessions, datetime(2026, 9, 28, 19))
        self.assertEqual(s.today, 1800)
        self.assertEqual(s.week, 1800)  # Woche beginnt Montag
        self.assertEqual(s.month, 3600 * 4.5)
        self.assertEqual(s.year, 3600 * 4.5)
        self.assertEqual(s.total, 3600 * 6.5)
        self.assertEqual(s.streak, 3)
        self.assertEqual(s.longest, 7200)

    def test_streak_survives_until_today_is_played(self) -> None:
        sessions = [(ts(2026, 9, 27, 20), ts(2026, 9, 27, 21))]
        self.assertEqual(summarize(sessions, datetime(2026, 9, 28, 9)).streak, 1)

    def test_bucket_labels(self) -> None:
        self.assertEqual([b.short for b in buckets("month", date(2026, 2, 10), 3)], ["DEZ", "JAN", "FEB"])
        self.assertEqual(buckets("week", date(2026, 9, 28), 1)[0].short, "40")
        self.assertEqual([b.short for b in buckets("year", date(2026, 1, 1), 2)], ["2025", "2026"])

    def test_format(self) -> None:
        self.assertEqual(fmt_hm(59 * 60), "59m")
        self.assertEqual(fmt_hm(3600 + 5 * 60), "1h 05m")
        self.assertEqual(fmt_clock(3 * 3600 + 7), "03:00:07")


class ChannelTest(unittest.TestCase):
    def test_star_citizen_channels(self) -> None:
        base = r"C:\Program Files\Roberts Space Industries\StarCitizen"
        for ch in ("LIVE", "PTU", "HOTFIX", "TECH-PREVIEW"):
            self.assertEqual(channel_from_path(rf"{base}\{ch}\Bin64\StarCitizen.exe"), ch)
        self.assertEqual(channel_from_path(r"D:\Games\Other\game.exe"), "")
        self.assertEqual(channel_from_path(None), "")

    def test_channel_order(self) -> None:
        self.assertEqual(sort_channels(["TECH-PREVIEW", "PTU", "X", "LIVE"]), ["LIVE", "PTU", "TECH-PREVIEW", "X"])


class TrackerTest(unittest.TestCase):
    def test_session_lifecycle_per_game_and_channel(self) -> None:
        running: dict[str, int] = {}
        paths = {1: r"C:\SC\StarCitizen\PTU\Bin64\StarCitizen.exe", 2: r"C:\G\other.exe"}
        store = Store(Path(":memory:"))
        tracker = Tracker(
            store,
            [Game("Star Citizen", "StarCitizen.exe"), Game("Other", "other.exe")],
            find=lambda names: {n.lower(): running[n.lower()] for n in names if n.lower() in running},
            start_time=lambda pid: 1000.0,
            image_path=paths.get,
        )
        running["starcitizen.exe"] = 1
        tracker.poll(now=1010.0)
        self.assertEqual(tracker.running(), ["Star Citizen"])
        self.assertEqual(tracker.live_channel("Star Citizen"), "PTU")
        tracker.poll(now=1100.0)
        del running["starcitizen.exe"]
        tracker.poll(now=1102.0)
        self.assertEqual(tracker.running(), [])
        self.assertEqual(tracker.sessions("Star Citizen"), [(1000.0, 1102.0)])
        self.assertEqual(tracker.sessions("Star Citizen", "LIVE"), [])
        self.assertEqual(tracker.channels("Star Citizen"), ["PTU"])
        self.assertEqual(store.all()[0].end, 1102.0)  # beim Beenden gespeichert
        self.assertEqual(tracker.sessions("Other"), [])

    def test_restart_resumes_same_session(self) -> None:
        store = Store(Path(":memory:"))
        make = lambda: Tracker(  # noqa: E731
            store, [Game("Star Citizen", "StarCitizen.exe")],
            find=lambda names: {"starcitizen.exe": 7}, start_time=lambda pid: 500.0, image_path=lambda pid: None,
        )
        make().poll(now=600.0)
        second = make()
        second.poll(now=700.0)
        self.assertEqual(len(store.all()), 1)
        self.assertEqual(second.sessions("Star Citizen"), [(500.0, 700.0)])


if __name__ == "__main__":
    unittest.main()
