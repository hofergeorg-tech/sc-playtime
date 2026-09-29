import os
import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sc_playtime import i18n, process  # noqa: E402
from sc_playtime.process import channel_from_path  # noqa: E402
from sc_playtime.stats import buckets, fmt_clock, fmt_hm, played, summarize  # noqa: E402
from sc_playtime.store import Store  # noqa: E402
from sc_playtime.tracker import Game, Tracker, sort_channels  # noqa: E402
from sc_playtime.updater import install_script, is_newer  # noqa: E402


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


class I18nTest(unittest.TestCase):
    def tearDown(self) -> None:
        i18n.set_language("de")

    def test_all_languages_have_all_keys_and_flags(self) -> None:
        root = Path(__file__).resolve().parent.parent
        for code in i18n.LANGUAGES:
            self.assertEqual(set(i18n.STRINGS[code]), set(i18n.STRINGS["de"]), code)
            self.assertTrue((root / "assets" / "flags" / f"{code}.svg").exists(), code)
            for doc in i18n.DOCS[code].values():
                self.assertTrue((root / doc).exists(), doc)

    def test_placeholders_match(self) -> None:
        import string

        fields = lambda s: {f for _, f, _, _ in string.Formatter().parse(s) if f}  # noqa: E731
        for code in i18n.LANGUAGES:
            for key, text in i18n.STRINGS[code].items():
                self.assertEqual(fields(text), fields(i18n.STRINGS["de"][key]), f"{code}:{key}")

    def test_switch_changes_labels(self) -> None:
        i18n.set_language("en")
        self.assertEqual([b.short for b in buckets("month", date(2026, 5, 10), 2)], ["APR", "MAY"])
        self.assertEqual(i18n.tr("upd.none", version="1.0"), "You have the latest version (1.0).")
        i18n.set_language("xx")  # unbekannt → Systemsprache, nie ein Absturz
        self.assertIn(i18n.language(), i18n.LANGUAGES)


class LinuxProcessTest(unittest.TestCase):
    def test_parsing_helpers(self) -> None:
        wine = b"C:\\Program Files\\Roberts Space Industries\\StarCitizen\\PTU\\Bin64\\StarCitizen.exe\0-arg\0"
        self.assertEqual(process.basename_any(process.argv0(wine)), "StarCitizen.exe")
        self.assertEqual(channel_from_path(process.argv0(wine)), "PTU")
        self.assertEqual(process.basename_any("/usr/games/foo"), "foo")
        stat = "1234 (Star Citizen (x)) S " + " ".join(["0"] * 18) + " 500 0 0"
        self.assertEqual(process.start_from_stat(stat, 1000.0, 100.0), 1005.0)
        self.assertIsNone(process.start_from_stat("kaputt", 0, 100))

    @unittest.skipUnless(sys.platform.startswith("linux"), "nur unter Linux")
    def test_finds_real_process(self) -> None:
        import subprocess
        import time

        proc = subprocess.Popen(["sleep", "30"])
        try:
            found = process.find_processes(["sleep"])
            self.assertIn("sleep", found)
            start = process.process_start_time(found["sleep"])
            self.assertIsNotNone(start)
            self.assertLess(abs(start - time.time()), 30)
        finally:
            proc.kill()

    @unittest.skipUnless(sys.platform.startswith("linux"), "nur unter Linux")
    def test_autostart_desktop_file(self) -> None:
        import tempfile

        from sc_playtime import autostart

        with tempfile.TemporaryDirectory() as tmp:
            os.environ["XDG_CONFIG_HOME"] = tmp
            try:
                autostart.set_enabled(True)
                self.assertTrue(autostart.is_enabled())
                entry = (Path(tmp) / "autostart" / "sc-playtime.desktop").read_text()
                self.assertIn("Exec=", entry)
                autostart.set_enabled(False)
                self.assertFalse(autostart.is_enabled())
            finally:
                del os.environ["XDG_CONFIG_HOME"]


class UiSmokeTest(unittest.TestCase):
    """Overlay und Menü in jeder Sprache aufbauen, ohne Bildschirm (offscreen)."""

    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        from PySide6 import QtWidgets

        cls.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    def test_overlay_and_menu_in_all_languages(self) -> None:
        from PySide6 import QtGui, QtWidgets

        from sc_playtime.settings import Settings
        from sc_playtime.ui import Overlay

        class FakeTracker:
            def running(self): return ["Star Citizen"]
            def live_channel(self, g): return "LIVE"
            def channels(self, g): return ["LIVE", "PTU"]
            def sessions(self, g, c): return [(ts(2026, 9, 28, 18), ts(2026, 9, 28, 19))]
            def current_duration(self, g, c): return 100.0

        for code in i18n.LANGUAGES:
            i18n.set_language(code)
            overlay = Overlay(FakeTracker(), Settings(expanded=True, language=code), lambda: None)
            image = QtGui.QImage(overlay.size(), QtGui.QImage.Format.Format_ARGB32_Premultiplied)
            overlay.render(image)
            menu = QtWidgets.QMenu()
            overlay.populate_menu(menu, tray=True)
            texts = [a.text() for a in menu.actions()]
            self.assertIn(i18n.tr("menu.quit"), texts)
            overlay.deleteLater()
        i18n.set_language("de")


class UpdaterTest(unittest.TestCase):
    def test_version_compare(self) -> None:
        self.assertTrue(is_newer("v1.10.0", "1.9.3"))
        self.assertTrue(is_newer("1.2.1", "1.2"))
        self.assertFalse(is_newer("1.2.0", "1.2.0"))
        self.assertFalse(is_newer("kaputt", "1.0.0"))

    def test_install_script_replaces_and_restarts(self) -> None:
        script = install_script(Path(r"C:\T\u\SC-Playtime.exe"), Path(r"D:\Apps\SC-Playtime.exe"))
        self.assertIn(r'move /Y "C:\T\u\SC-Playtime.exe" "D:\Apps\SC-Playtime.exe"', script)
        self.assertIn(r'start "" "D:\Apps\SC-Playtime.exe"', script)
        self.assertNotIn("start", install_script(Path("a"), Path("b"), restart=False))


if __name__ == "__main__":
    unittest.main()
