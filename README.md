# SC Playtime

🇬🇧 [English](README.en.md)

Mini-Overlay im Star-Citizen-HUD-Stil, das die Spielzeit erfasst – für **Windows** und
**Linux**, auf **Deutsch** und **Englisch**.

📥 **[Download](https://github.com/hofergeorg-tech/sc-playtime/releases/latest)** ·
📖 **[Hilfe – alle Funktionen erklärt](HILFE.md)** · 📝 **[Changelog](CHANGELOG.md)**

- erkennt `StarCitizen.exe` automatisch (alle 2 s, nur Prozessliste lesen) – unter Linux
  auch über Wine/Proton/Lutris
- **Channel aus dem Installationsordner**: `…\StarCitizen\LIVE\Bin64\StarCitizen.exe` → LIVE,
  ebenso PTU, EPTU, HOTFIX, TECH-PREVIEW — getrennt auswertbar oder zusammen („ALLE“)
- **mehrere Spiele**: beliebige weitere Programme über Rechtsklick → Spiel → Spiel hinzufügen …
- Anzeige: laufende Session (große Uhr), Heute / Woche; aufgeklappt: Monat, Jahr, Gesamt,
  Serie (Tage am Stück), Sessions, Ø- und längste Session, Balkendiagramm
  Tag (14) / Woche (12) / Monat (12) / Jahr (5) mit Hover-Werten
- Transparenz: Hintergrund und Gesamt-Deckkraft getrennt per Schieberegler
- Farben: Statistik-Kacheln werden im Spiel eingefärbt (Standard Grün mit dunkler Schrift),
  Kacheln und aktiver Channel-Chip per Vorlage oder freier Farbwahl einstellbar
- Sprache: Deutsch / English mit Flaggen im Menü, oder automatisch nach System
- Autostart (Windows: HKCU\…\Run, Linux: `~/.config/autostart`), Tray-Icon, Einzelinstanz
- Update-Prüfung über GitHub Releases mit Selbst-Update; Hilfe und „Was ist neu?“
  direkt im Menü

## Start aus dem Quellcode

```powershell
# Windows
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pythonw.exe run.pyw
```

```bash
# Linux
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.pyw
```

Star Citizen muss im **Fenstermodus randlos** laufen, sonst kann kein Overlay darüber
gezeichnet werden (gilt für alle Overlays). Linux-Besonderheiten (Wayland, GNOME-Tray):
siehe [Hilfe → Linux](HILFE.md#linux).

## Daten

Windows `%APPDATA%\SC-Playtime\`, Linux `~/.local/share/SC-Playtime/`

- `playtime.db` — SQLite, Tabelle `sessions(game, channel, start, end)`
- `settings.json` — Position, Transparenz, Farben, Sprache, Spieleliste …

## Programm bauen

```powershell
.venv\Scripts\pip install pyinstaller
.venv\Scripts\python.exe build.py      # → dist\SC-Playtime.exe (Linux: dist/SC-Playtime)
```

## Release veröffentlichen

1. Version in `sc_playtime/__init__.py` erhöhen, `CHANGELOG.md` und `CHANGELOG.en.md` ergänzen.
2. Committen, Tag setzen und pushen: `git tag v1.4.0 && git push --tags`
3. GitHub Actions ([ci.yml](.github/workflows/ci.yml)) testet, baut Windows- und
   Linux-Programm und legt das Release mit beiden Dateien an. Die installierten
   Overlays finden das Update dann von selbst.

## Übersetzen

Texte stehen in [sc_playtime/i18n.py](sc_playtime/i18n.py). Neue Sprache: Tabelle
ergänzen, Flagge als `assets/flags/<code>.svg` ablegen, optional Hilfe/Changelog
übersetzen und in `DOCS` eintragen.

## Tests

```powershell
python -m unittest discover -s tests
```
