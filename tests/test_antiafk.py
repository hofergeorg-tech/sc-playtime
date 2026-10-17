"""Tests für Anti-AFK: nur bei echtem Leerlauf, nur mit dem Spiel im Vordergrund."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sc_playtime.antiafk import PATTERNS, AntiAfk, mouse_path, unit_steps  # noqa: E402
from sc_playtime.settings import Settings  # noqa: E402


class FakePc:
    """Uhr (ms), letzte Eingabe und Vordergrundfenster wie bei Windows."""

    def __init__(self) -> None:
        self.now = 1_000_000
        self.last = self.now
        self.front = "StarCitizen.exe"
        self.sent: list[str] = []

    def user_input(self) -> None:
        self.last = self.now

    def wait(self, seconds: float) -> None:
        self.now += int(seconds * 1000)

    def anti(self, settings: Settings) -> AntiAfk:
        def inject(kind: str):
            def run(*_args) -> None:
                self.sent.append(kind)
                self.now += 60
                self.last = self.now  # eigene Eingaben setzen GetLastInputInfo ebenfalls
            return run

        return AntiAfk(settings, lambda: ["StarCitizen.exe"], last_input=lambda: self.last, tick=lambda: self.now,
                       foreground_exe=lambda: self.front, send_key=inject("key"), move_mouse=inject("mouse"),
                       run_async=lambda fn: fn())


class AntiAfkTest(unittest.TestCase):
    def test_off_by_default(self) -> None:
        pc = FakePc()
        anti = pc.anti(Settings())
        pc.wait(3600)
        self.assertEqual(anti.poll(), [])
        self.assertEqual(pc.sent, [])
        settings = Settings(anti_afk_mouse=True)  # Aktionen gewählt, Hauptschalter aus
        anti = pc.anti(settings)
        self.assertEqual(anti.poll(), [])
        settings.anti_afk_on = True  # z. B. per Tastenkürzel
        self.assertEqual(anti.poll(), ["mouse", "key"])

    def test_key_every_5_seconds(self) -> None:
        pc = FakePc()
        anti = pc.anti(Settings(anti_afk_on=True, anti_afk_key=True))
        self.assertEqual(anti.poll(), ["key"])  # sofort beim Einschalten
        for _ in range(9):
            pc.wait(0.5)
            self.assertEqual(anti.poll(), [])
        pc.wait(0.5)
        self.assertEqual(anti.poll(), ["key"])

    def test_separate_intervals(self) -> None:
        pc = FakePc()
        anti = pc.anti(Settings(anti_afk_on=True, anti_afk_key=True, anti_afk_key_s=5,
                                anti_afk_mouse=True, anti_afk_mouse_s=60))
        anti.poll()
        for _ in range(118):  # 59 s
            pc.wait(0.5)
            anti.poll()
        self.assertEqual(pc.sent.count("mouse"), 1)
        self.assertEqual(pc.sent.count("key"), 12)  # bei 0, 5 … 55 s

    def test_own_input_does_not_count_as_activity(self) -> None:
        pc = FakePc()
        anti = pc.anti(Settings(anti_afk_on=True, anti_afk_key=False, anti_afk_mouse=True, anti_afk_mouse_s=60))
        pc.wait(61)
        anti.poll()
        pc.wait(10)
        # 71 s echter Leerlauf, obwohl die letzte (eigene) Eingabe erst 10 s her ist
        self.assertAlmostEqual(anti.idle_seconds(), 71.06, places=2)

    def test_runs_while_playing(self) -> None:
        pc = FakePc()
        anti = pc.anti(Settings(anti_afk_on=True, anti_afk_key=True, anti_afk_key_s=5))
        for _ in range(40):  # 20 s lang ständig eigene Eingaben
            pc.user_input()
            anti.poll()
            pc.wait(0.5)
        self.assertEqual(pc.sent.count("key"), 4)
        self.assertLess(anti.idle_seconds(), 1)

    def test_only_with_game_in_foreground(self) -> None:
        pc = FakePc()
        anti = pc.anti(Settings(anti_afk_on=True, anti_afk_key=True))
        pc.front = "Discord.exe"
        pc.wait(300)
        self.assertEqual(anti.poll(), [])
        pc.front = "starcitizen.EXE"
        self.assertEqual(anti.poll(), ["key"])

    def test_tick_overflow(self) -> None:
        pc = FakePc()
        pc.now = pc.last = 0xFFFFFFFF - 1000
        anti = pc.anti(Settings(anti_afk_on=True, anti_afk_key=False, anti_afk_mouse=True, anti_afk_mouse_s=60))
        pc.now = (pc.now + 61_000) & 0xFFFFFFFF
        self.assertAlmostEqual(anti.idle_seconds(), 61.0)
        self.assertEqual(anti.poll(), ["mouse"])

    def test_mouse_paths_return_to_start(self) -> None:
        for pattern in PATTERNS:
            for px in (1, 2, 5, 37, 100, 500):
                steps = mouse_path(pattern, px, rng=lambda: 0.3)
                self.assertTrue(steps, (pattern, px))
                self.assertEqual((sum(x for x, _ in steps), sum(y for _, y in steps)), (0, 0), (pattern, px))
                self.assertLessEqual(max(max(abs(x), abs(y)) for x, y in steps), 100)
        self.assertEqual(mouse_path("horizontal", 7), [(7, 0), (-7, 0)])
        self.assertEqual(mouse_path("vertical", 7), [(0, 7), (0, -7)])
        self.assertEqual(mouse_path("unknown", 3), [(3, 0), (-3, 0)])

    def test_unit_steps_glide_pixel_by_pixel(self) -> None:
        for pattern in PATTERNS:
            units = unit_steps(mouse_path(pattern, 40, rng=lambda: 0.7))
            self.assertTrue(all(max(abs(x), abs(y)) <= 1 for x, y in units), pattern)
            self.assertEqual((sum(x for x, _ in units), sum(y for _, y in units)), (0, 0), pattern)
        self.assertEqual(len(unit_steps([(5, 0), (-5, 0)])), 10)


class RingClickTest(unittest.TestCase):
    def test_click_toggles_actions(self) -> None:
        import os
        import tempfile

        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        from PySide6 import QtWidgets

        from sc_playtime.store import Store
        from sc_playtime.tracker import Game, Tracker
        from sc_playtime.ui import Overlay

        QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        tracker = Tracker(Store(Path(tempfile.mkdtemp()) / "x.db"), [Game("Star Citizen", "StarCitizen.exe")],
                          find=lambda _n: {})
        s = Settings(anti_afk_key=True, anti_afk_mouse=True)
        overlay = Overlay(tracker, s, lambda: None)
        state = lambda: (s.anti_afk_on, s.anti_afk_key, s.anti_afk_mouse)  # noqa: E731
        overlay.toggle_anti_afk_action("mouse")  # alles aus → nur die Maus an
        self.assertEqual(state(), (True, False, True))
        overlay.toggle_anti_afk_action("key")  # Taste dazu
        self.assertEqual(state(), (True, True, True))
        overlay.toggle_anti_afk_action("mouse")  # Maus weg
        self.assertEqual(state(), (True, True, False))
        overlay.toggle_anti_afk_action("key")  # letzte Aktion → ganz aus, Auswahl bleibt
        self.assertEqual(state(), (False, True, False))


if __name__ == "__main__":
    unittest.main()
