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


class AnalysisTest(unittest.TestCase):
    def test_buckets_with_offset(self) -> None:
        days = buckets("day", date(2026, 9, 28), 3, offset=2)
        self.assertEqual([b.short for b in days], ["24", "25", "26"])
        self.assertEqual(buckets("month", date(2026, 2, 10), 1, offset=2)[0].short, "DEZ")

    def test_max_offset(self) -> None:
        from sc_playtime.stats import max_offset, periods_back

        today = date(2026, 9, 28)  # Montag
        self.assertEqual(periods_back("week", date(2026, 9, 27), today), 1)  # Sonntag der Vorwoche
        self.assertEqual(periods_back("week", date(2026, 9, 20), today), 2)
        self.assertEqual(periods_back("month", date(2025, 11, 30), today), 10)
        self.assertEqual(max_offset("day", date(2026, 9, 1), today, 14), 27 - 13)
        self.assertEqual(max_offset("day", date(2026, 9, 25), today, 14), 0)

    def test_heatmap_splits_hours(self) -> None:
        from sc_playtime.stats import heatmap

        grid = heatmap([(ts(2026, 9, 28, 22, 30), ts(2026, 9, 29, 0, 15))])  # Mo 22:30 – Di 0:15
        self.assertEqual(grid[0][22], 1800)
        self.assertEqual(grid[0][23], 3600)
        self.assertEqual(grid[1][0], 900)
        self.assertEqual(sum(map(sum, grid)), 6300)

    def test_by_version_newest_first_unknown_last(self) -> None:
        from sc_playtime.stats import by_version

        rows = [("", 0, 100), ("4.2.1", 100, 400), ("4.10.0", 500, 600), ("4.2.1", 700, 900)]
        stats = by_version(rows)
        self.assertEqual([p.version for p in stats], ["4.10.0", "4.2.1", ""])
        self.assertEqual(stats[1].total, 500)
        self.assertEqual((stats[1].first, stats[1].last), (100, 900))


class StoreTest(unittest.TestCase):
    def test_migrates_old_database(self) -> None:
        import sqlite3
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "playtime.db"
            db = sqlite3.connect(path)  # Schema bis 1.3.x
            db.execute("CREATE TABLE sessions (id INTEGER PRIMARY KEY, game TEXT NOT NULL,"
                       " channel TEXT NOT NULL DEFAULT '', start REAL NOT NULL, end REAL NOT NULL)")
            db.execute("INSERT INTO sessions(game, channel, start, end) VALUES ('Star Citizen', 'LIVE', 1, 2)")
            db.commit()
            db.close()
            store = Store(path)
            self.assertEqual(store.all()[0].version, "")
            store.close()

    def test_edit_delete_and_backup(self) -> None:
        import tempfile

        from sc_playtime import backup

        store = Store(Path(":memory:"))
        a = store.open("G", "", 100.0, 200.0, "4.3.1")
        b = store.open("G", "", 1000.0, 1100.0)
        store.update(a.id, 50.0, 250.0)
        store.delete(b.id)
        self.assertEqual([(r.start, r.end, r.version) for r in store.all()], [(50.0, 250.0, "4.3.1")])

        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for day in range(1, 10):
                backup.run(store, folder, date(2026, 9, day), keep=7)
            files = sorted(p.name for p in folder.glob("*.db"))
            self.assertEqual(files[0], "playtime-2026-09-03.db")
            self.assertEqual(len(files), 7)
            self.assertIsNone(backup.run(store, folder, date(2026, 9, 9)))  # heute schon gesichert
            copy = Store(folder / files[-1])
            self.assertEqual(len(copy.all()), 1)
            copy.close()


class ExportTest(unittest.TestCase):
    def test_csv_and_json(self) -> None:
        import json

        from sc_playtime.export import to_csv, to_json
        from sc_playtime.store import SessionRow

        rows = [SessionRow(1, "Star Citizen", "LIVE", ts(2026, 9, 28, 18), ts(2026, 9, 28, 19, 30), "4.3.1")]
        lines = to_csv(rows).splitlines()
        self.assertEqual(lines[0], "game;channel;version;start;end;duration_s;duration_min")
        self.assertEqual(lines[1], "Star Citizen;LIVE;4.3.1;2026-09-28 18:00:00;2026-09-28 19:30:00;5400;90")
        self.assertIn(",LIVE,", to_csv(rows, ",").splitlines()[1])
        data = json.loads(to_json(rows))["sessions"][0]
        self.assertEqual(data["duration_s"], 5400)
        self.assertTrue(data["start"].startswith("2026-09-28T18:00:00"))


class HotkeyTest(unittest.TestCase):
    def test_parse(self) -> None:
        from sc_playtime.hotkeys import MOD_ALT, MOD_CONTROL, MOD_SHIFT, parse

        self.assertEqual(parse("Ctrl+Shift+F9"), (MOD_CONTROL | MOD_SHIFT, 0x78))
        self.assertEqual(parse("Alt+P"), (MOD_ALT, ord("P")))
        self.assertEqual(parse("F12"), (0, 0x7B))  # F-Tasten auch ohne Zusatztaste
        self.assertIsNone(parse("P"))  # normales Tippen nicht abfangen
        self.assertIsNone(parse("Ctrl+ä"))
        self.assertIsNone(parse(""))


class ChannelTest(unittest.TestCase):
    def test_version_from_install_folder(self) -> None:
        import tempfile

        manifest = '{"Data": {"Branch": "sc-alpha-4.3.1", "Version": "4.3.1.10044599"}}'
        self.assertEqual(process.version_from_manifest(manifest), "4.3.1")
        self.assertEqual(process.version_from_manifest('{"Data": {"Version": "4.2.0.1"}}'), "4.2.0")
        self.assertEqual(process.version_from_manifest("kaputt"), "")
        self.assertEqual(process.version_from_log(["<x> Log started", "Branch: sc-alpha-4.1.1"]), "4.1.1")
        with tempfile.TemporaryDirectory() as tmp:
            live = Path(tmp) / "LIVE"
            (live / "Bin64").mkdir(parents=True)
            (live / "Game.log").write_text("Branch: sc-alpha-4.0.2\n", encoding="utf-8")
            self.assertEqual(process.version_in_dirs([live / "Bin64", live]), "4.0.2")
            (live / "build_manifest.id").write_text(manifest, encoding="utf-8")
            self.assertEqual(process.version_in_dirs([live]), "4.3.1")
            self.assertEqual(process.version_in_dirs([Path(tmp) / "fehlt"]), "")

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

    def _afk_tracker(self, store: Store, idle: list[float]) -> Tracker:
        return Tracker(
            store, [Game("Star Citizen", "StarCitizen.exe")],
            find=lambda names: {"starcitizen.exe": 7}, start_time=lambda pid: 1000.0,
            image_path=lambda pid: r"C:\SC\StarCitizen\LIVE\Bin64\StarCitizen.exe",
            version=lambda pid: "4.3.1", idle=lambda: idle[0], afk_s=300.0,
        )

    def test_afk_splits_session(self) -> None:
        store = Store(Path(":memory:"))
        idle = [0.0]
        tracker = self._afk_tracker(store, idle)
        tracker.poll(now=1100.0)
        idle[0] = 400.0  # letzte Eingabe bei 1600
        tracker.poll(now=2000.0)
        self.assertTrue(tracker.is_afk("Star Citizen"))
        self.assertEqual(tracker.running(), ["Star Citizen"])  # Spiel läuft weiter
        self.assertEqual(tracker.live_channel("Star Citizen"), "LIVE")
        tracker.poll(now=2500.0)  # weiter AFK: nichts zählt
        idle[0] = 10.0  # wieder da seit 2990
        tracker.poll(now=3000.0)
        self.assertFalse(tracker.is_afk("Star Citizen"))
        self.assertEqual(tracker.sessions("Star Citizen"), [(1000.0, 1600.0), (2990.0, 3000.0)])
        self.assertEqual([r.version for r in store.all()], ["4.3.1", "4.3.1"])
        # Overlay-Neustart während das Spiel läuft: die letzte Teil-Session wird fortgesetzt
        restarted = self._afk_tracker(store, [0.0])
        restarted.poll(now=3100.0)
        self.assertEqual(restarted.sessions("Star Citizen"), [(1000.0, 1600.0), (2990.0, 3100.0)])

    def test_afk_at_game_start_records_nothing(self) -> None:
        store = Store(Path(":memory:"))
        idle = [900.0]
        tracker = self._afk_tracker(store, idle)
        tracker.poll(now=2000.0)
        self.assertEqual(store.all(), [])
        idle[0] = 0.0
        tracker.poll(now=2100.0)
        self.assertEqual(tracker.sessions("Star Citizen"), [(2100.0, 2100.0)])
        self.assertEqual(tracker.live_channel("Star Citizen"), "LIVE")

    def test_edit_and_delete_sessions(self) -> None:
        store = Store(Path(":memory:"))
        running = {"starcitizen.exe": 7}
        tracker = Tracker(store, [Game("Star Citizen", "StarCitizen.exe")],
                          find=lambda names: dict(running), start_time=lambda pid: 1000.0,
                          image_path=lambda pid: None, version=lambda pid: "", idle=lambda: None)
        tracker.poll(now=1100.0)
        live_id = store.all()[0].id
        with self.assertRaises(ValueError):
            tracker.delete_session(live_id)  # laufende Session ist gesperrt
        running.clear()
        tracker.poll(now=1200.0)
        tracker.update_session(live_id, 900.0, 1300.0)
        self.assertEqual(tracker.sessions("Star Citizen"), [(900.0, 1300.0)])
        with self.assertRaises(ValueError):
            tracker.update_session(live_id, 1300.0, 900.0)
        tracker.delete_session(live_id)
        self.assertEqual((tracker.sessions("Star Citizen"), store.all()), ([], []))


class I18nTest(unittest.TestCase):
    def tearDown(self) -> None:
        i18n.set_language("de")

    def test_all_languages_have_all_keys_and_flags(self) -> None:
        root = Path(__file__).resolve().parent.parent
        for code in i18n.LANGUAGES:
            self.assertEqual(set(i18n.STRINGS[code]), set(i18n.STRINGS["de"]), code)
            self.assertTrue((root / "assets" / "flags" / f"{code}.svg").exists(), code)
            self.assertEqual(len(i18n.STRINGS[code]["weekdays"].split()), 7, code)
            self.assertEqual(len(i18n.STRINGS[code]["months"].split()), 12, code)
            i18n.set_language(code)
            for kind in ("help", "changelog"):
                self.assertTrue((root / i18n.doc_file(kind)).exists(), f"{code}:{kind}")
        self.assertEqual(set(i18n.DOCS) - set(i18n.LANGUAGES), set())

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

        from sc_playtime import dialogs
        from sc_playtime.ui import app_icon

        sessions = [(ts(2026, 9, 28, 18), ts(2026, 9, 28, 19))]

        class FakeTracker:
            afk = False
            def running(self): return ["Star Citizen"]
            def is_afk(self, g): return self.afk
            def live_channel(self, g): return "LIVE"
            def channels(self, g): return ["LIVE", "PTU"]
            def sessions(self, g, c=""): return sessions
            revision = 0
            def closed_sessions(self, g, c=""): return self.sessions(g, c)
            def live_span(self, g, c=""): return None
            def versioned(self, g, c=""): return [("4.3.1", *sessions[0])]
            def rows(self, g=None): return []
            def is_live(self, i): return False
            def current_duration(self, g, c): return 100.0

        for code in i18n.LANGUAGES:
            i18n.set_language(code)
            tracker = FakeTracker()
            overlay = Overlay(tracker, Settings(expanded=True, language=code), lambda: None)
            image = QtGui.QImage(overlay.size(), QtGui.QImage.Format.Format_ARGB32_Premultiplied)
            overlay.render(image)
            overlay._hover = len(overlay._bars) - 1  # Fußzeile mit Hover-Text
            overlay.render(image)
            tracker.afk = True  # Kopf im AFK-Zustand
            overlay.refresh()
            overlay.render(image)
            menu = QtWidgets.QMenu()
            overlay.populate_menu(menu, tray=True)
            texts = [a.text() for a in menu.actions()]
            self.assertIn(i18n.tr("menu.quit"), texts)
            self.assertIn(i18n.tr("menu.about"), texts)
            # Zusatzfenster in jeder Sprache aufbauen
            for win in (dialogs.AboutDialog(app_icon()),
                        dialogs.StatsDialog("Star Citizen", "", sessions, tracker.versioned(""), app_icon()),
                        dialogs.SessionsDialog(tracker, "Star Citizen", lambda: None, app_icon()),
                        dialogs.HotkeyDialog(Settings())):
                win.grab()
                win.deleteLater()
            overlay.deleteLater()
        i18n.set_language("de")

    def test_chart_scrolls_back_to_first_session(self) -> None:
        from sc_playtime.settings import Settings
        from sc_playtime.ui import Overlay

        first = datetime.combine(date.today(), datetime.min.time()).timestamp() - 30 * 86400 + 3600

        class FakeTracker:
            def running(self): return []
            def is_afk(self, g): return False
            def live_channel(self, g): return None
            def channels(self, g): return []
            def sessions(self, g, c=""): return [(first, first + 3600)]
            revision = 0
            def closed_sessions(self, g, c=""): return self.sessions(g, c)
            def live_span(self, g, c=""): return None
            def current_duration(self, g, c): return 0.0

        overlay = Overlay(FakeTracker(), Settings(expanded=True, tab="day"), lambda: None)
        self.assertEqual(overlay._max_offset, 30 - 13)  # ältester Balken = Tag der ersten Session
        overlay.scroll_chart(100)
        self.assertEqual(overlay._offset, 17)
        self.assertEqual(overlay._bars[0][1], 3600.0)
        overlay.scroll_chart(-100)
        self.assertEqual(overlay._offset, 0)
        overlay.deleteLater()

    def test_channel_filter_keeps_common_scale(self) -> None:
        """PTU-Filter: Balken nur PTU, Skala/Schatten aber nach allen Channels."""
        from PySide6 import QtGui

        from sc_playtime.settings import Settings
        from sc_playtime.ui import Overlay

        midnight = datetime.combine(date.today(), datetime.min.time()).timestamp()
        live = (midnight + 3600, midnight + 3 * 3600)  # heute 2 h LIVE
        ptu = (midnight + 3 * 3600, midnight + 3 * 3600 + 360)  # heute 6 min PTU

        class FakeTracker:
            def running(self): return []
            def is_afk(self, g): return False
            def live_channel(self, g): return None
            def channels(self, g): return ["LIVE", "PTU"]
            def sessions(self, g, c=""): return {"": [live, ptu], "LIVE": [live], "PTU": [ptu]}[c]
            revision = 0
            def closed_sessions(self, g, c=""): return self.sessions(g, c)
            def live_span(self, g, c=""): return None
            def current_duration(self, g, c): return 0.0

        overlay = Overlay(FakeTracker(), Settings(expanded=True, channel="PTU"), lambda: None)
        (_, today_ptu), today_all = overlay._bars[-1], overlay._totals[-1]
        self.assertEqual((today_ptu, today_all), (360.0, 2 * 3600 + 360.0))
        overlay._hover = len(overlay._bars) - 1
        overlay.render(QtGui.QImage(overlay.size(), QtGui.QImage.Format.Format_ARGB32_Premultiplied))
        overlay.deleteLater()


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
