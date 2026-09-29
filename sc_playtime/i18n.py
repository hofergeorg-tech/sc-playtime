"""Mehrsprachigkeit: Texttabellen je Sprache, zur Laufzeit umschaltbar.

Neue Sprache: Eintrag in ``LANGUAGES``, Tabelle in ``STRINGS`` (alle Schlüssel
wie bei "de"), Flagge ``assets/flags/<code>.svg`` und optional übersetzte Hilfe
in ``DOCS``. Fehlende Schlüssel fallen auf Deutsch zurück.
"""

from __future__ import annotations

import locale
import os

# Code → Name in der eigenen Sprache (so erscheint er im Menü)
LANGUAGES = {"de": "Deutsch", "en": "English"}
DEFAULT = "de"

# Hilfe und Changelog je Sprache (liegen im Projektordner bzw. in der EXE)
DOCS = {
    "de": {"help": "HILFE.md", "changelog": "CHANGELOG.md"},
    "en": {"help": "HELP.md", "changelog": "CHANGELOG.en.md"},
}

_current = DEFAULT


def system_language() -> str:
    """Sprache des Betriebssystems, sofern unterstützt, sonst Englisch."""
    candidates = [os.environ.get(v, "") for v in ("LC_ALL", "LC_MESSAGES", "LANG")]
    try:
        candidates.append(locale.getlocale()[0] or "")
    except ValueError:
        pass
    if os.name == "nt":
        import ctypes

        lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        candidates.insert(0, locale.windows_locale.get(lcid, ""))
    for c in candidates:
        code = c.split("_")[0].split("-")[0].lower()
        if code in LANGUAGES:
            return code
        if c.lower().startswith("german"):
            return "de"
    return "en"


def set_language(code: str) -> None:
    """``""`` = automatisch nach System."""
    global _current
    _current = code if code in LANGUAGES else system_language()


def language() -> str:
    return _current


def tr(key: str, **kw: object) -> str:
    text = STRINGS[_current].get(key) or STRINGS[DEFAULT][key]
    return text.format(**kw) if kw else text


def tr_list(key: str) -> list[str]:
    return tr(key).split()


def doc_file(kind: str) -> str:
    return DOCS.get(_current, DOCS[DEFAULT])[kind]


STRINGS: dict[str, dict[str, str]] = {
    "de": {
        # Overlay
        "tab.day": "TAG", "tab.week": "WOCHE", "tab.month": "MONAT", "tab.year": "JAHR", "tab.total": "GESAMT",
        "hud.today": "HEUTE", "hud.week": "WOCHE", "hud.month": "MONAT", "hud.year": "JAHR",
        "hud.total": "GESAMT", "hud.streak": "SERIE", "hud.day": "TAG", "hud.days": "TAGE",
        "hud.all": "ALLE", "hud.in_game": "IM SPIEL", "hud.offline": "OFFLINE",
        "hud.max": "MAX {value}", "hud.no_data": "KEINE DATEN",
        "hud.footer": "SESSIONS {count}   ·   Ø {average}   ·   LÄNGSTE {longest}",
        "status": "SC Playtime · {game} {state} · Heute {today}",
        "status.active": "AKTIV", "status.offline": "offline",
        # Menü
        "menu.show": "Overlay einblenden", "menu.hide": "Overlay ausblenden",
        "menu.expanded": "Statistik aufgeklappt",
        "menu.game": "Spiel", "menu.add_game": "Spiel hinzufügen …", "menu.remove_game": "Spiel entfernen",
        "menu.background": "HINTERGRUND", "menu.opacity": "DECKKRAFT GESAMT",
        "menu.colors": "Farben", "menu.colors_tiles": "Statistik-Kacheln (im Spiel)",
        "menu.colors_chip": "Aktiver Channel",
        "menu.pick_bg": "Hintergrundfarbe wählen …", "menu.pick_fg": "Schriftfarbe wählen …",
        "color.bg": "Hintergrundfarbe", "color.fg": "Schriftfarbe",
        "preset.chip_auto": "Automatisch (Channel-Farbe, dunkle Schrift)",
        "preset.darkgreen_white": "Dunkelgrün / Weiß", "preset.black_green": "Schwarz / Grün",
        "preset.darkblue_white": "Dunkelblau / Weiß", "preset.white_black": "Weiß / Schwarz",
        "preset.green_dark": "Grün / Dunkel", "preset.cyan_dark": "Cyan / Dunkel",
        "preset.amber_dark": "Bernstein / Dunkel", "preset.tile_off": "Nicht einfärben (HUD)",
        "menu.lock": "Position sperren",
        "menu.click_through": "Klicks durchlassen (nur über Tray zurück)",
        "menu.hide_offline": "Nur anzeigen, wenn ein Spiel läuft",
        "menu.autostart_win": "Mit Windows starten", "menu.autostart_other": "Beim Anmelden starten",
        "menu.language": "Sprache", "lang.auto": "Automatisch (System)",
        "menu.help": "Hilfe …", "menu.changelog": "Was ist neu? …",
        "menu.check_updates": "Nach Updates suchen", "menu.auto_update": "Automatisch nach Updates suchen",
        "menu.install_update": "⬆  Update auf {version} installieren …",
        "menu.data_folder": "Datenordner öffnen", "menu.quit": "Beenden",
        # Spiele
        "game.pick_exe": "Programm des Spiels wählen", "game.filter_exe": "Programme (*.exe)",
        "game.filter_all": "Alle Dateien (*)",
        "game.add_title": "Spiel hinzufügen", "game.display_name": "Anzeigename:",
        "game.remove_title": "Spiel entfernen",
        "game.remove_text": "»{name}« nicht mehr verfolgen?\nBisherige Sessions bleiben gespeichert.",
        # Updates
        "upd.check_failed_title": "Update-Prüfung fehlgeschlagen",
        "upd.unreachable": "GitHub war nicht erreichbar:\n{error}",
        "upd.available_title": "Update verfügbar",
        "upd.notify": "SC Playtime {new} ist da (installiert: {current}).\n"
                      "Hier klicken oder Rechtsklick → Update installieren.",
        "upd.none_title": "Kein Update", "upd.none": "Du hast die neueste Version ({version}).",
        "upd.question": "SC Playtime {new} ist verfügbar (installiert: {current}).",
        "upd.confirm_self": "Jetzt herunterladen und installieren? Das Overlay startet danach neu, "
                            "die laufende Session wird vorher gespeichert.",
        "upd.confirm_browser": "Die Release-Seite wird im Browser geöffnet.",
        "upd.downloading": "Update wird heruntergeladen …",
        "upd.failed_title": "Update fehlgeschlagen", "upd.download_failed": "Download fehlgeschlagen:\n{error}",
        # Hilfe-Fenster
        "doc.help": "Hilfe", "doc.changelog": "Was ist neu?", "doc.close": "Schließen",
        "doc.missing": "*{file} nicht gefunden.*",
        # Statistik-Beschriftungen
        "weekdays": "MO DI MI DO FR SA SO",
        "months": "JAN FEB MÄR APR MAI JUN JUL AUG SEP OKT NOV DEZ",
        "fmt.date": "%d.%m.%Y", "fmt.date_short": "%d.%m.",
        "week.long": "KW {week} · {start}–{end}",
    },
    "en": {
        "tab.day": "DAY", "tab.week": "WEEK", "tab.month": "MONTH", "tab.year": "YEAR", "tab.total": "TOTAL",
        "hud.today": "TODAY", "hud.week": "WEEK", "hud.month": "MONTH", "hud.year": "YEAR",
        "hud.total": "TOTAL", "hud.streak": "STREAK", "hud.day": "DAY", "hud.days": "DAYS",
        "hud.all": "ALL", "hud.in_game": "IN GAME", "hud.offline": "OFFLINE",
        "hud.max": "MAX {value}", "hud.no_data": "NO DATA",
        "hud.footer": "SESSIONS {count}   ·   AVG {average}   ·   LONGEST {longest}",
        "status": "SC Playtime · {game} {state} · Today {today}",
        "status.active": "ACTIVE", "status.offline": "offline",
        "menu.show": "Show overlay", "menu.hide": "Hide overlay",
        "menu.expanded": "Show statistics",
        "menu.game": "Game", "menu.add_game": "Add game …", "menu.remove_game": "Remove game",
        "menu.background": "BACKGROUND", "menu.opacity": "OVERALL OPACITY",
        "menu.colors": "Colors", "menu.colors_tiles": "Statistic tiles (in game)",
        "menu.colors_chip": "Active channel",
        "menu.pick_bg": "Choose background color …", "menu.pick_fg": "Choose text color …",
        "color.bg": "Background color", "color.fg": "Text color",
        "preset.chip_auto": "Automatic (channel color, dark text)",
        "preset.darkgreen_white": "Dark green / White", "preset.black_green": "Black / Green",
        "preset.darkblue_white": "Dark blue / White", "preset.white_black": "White / Black",
        "preset.green_dark": "Green / Dark", "preset.cyan_dark": "Cyan / Dark",
        "preset.amber_dark": "Amber / Dark", "preset.tile_off": "No highlight (HUD)",
        "menu.lock": "Lock position",
        "menu.click_through": "Click-through (undo via tray only)",
        "menu.hide_offline": "Only show while a game is running",
        "menu.autostart_win": "Start with Windows", "menu.autostart_other": "Start on login",
        "menu.language": "Language", "lang.auto": "Automatic (system)",
        "menu.help": "Help …", "menu.changelog": "What's new? …",
        "menu.check_updates": "Check for updates", "menu.auto_update": "Check for updates automatically",
        "menu.install_update": "⬆  Install update {version} …",
        "menu.data_folder": "Open data folder", "menu.quit": "Quit",
        "game.pick_exe": "Choose the game's program", "game.filter_exe": "Programs (*.exe)",
        "game.filter_all": "All files (*)",
        "game.add_title": "Add game", "game.display_name": "Display name:",
        "game.remove_title": "Remove game",
        "game.remove_text": "Stop tracking “{name}”?\nExisting sessions are kept.",
        "upd.check_failed_title": "Update check failed",
        "upd.unreachable": "Could not reach GitHub:\n{error}",
        "upd.available_title": "Update available",
        "upd.notify": "SC Playtime {new} is available (installed: {current}).\n"
                      "Click here or right-click → Install update.",
        "upd.none_title": "No update", "upd.none": "You have the latest version ({version}).",
        "upd.question": "SC Playtime {new} is available (installed: {current}).",
        "upd.confirm_self": "Download and install now? The overlay restarts afterwards; "
                            "the running session is saved first.",
        "upd.confirm_browser": "The release page will open in your browser.",
        "upd.downloading": "Downloading update …",
        "upd.failed_title": "Update failed", "upd.download_failed": "Download failed:\n{error}",
        "doc.help": "Help", "doc.changelog": "What's new?", "doc.close": "Close",
        "doc.missing": "*{file} not found.*",
        "weekdays": "MO TU WE TH FR SA SU",
        "months": "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC",
        "fmt.date": "%d/%m/%Y", "fmt.date_short": "%d/%m",
        "week.long": "WK {week} · {start}–{end}",
    },
}
