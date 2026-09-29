# SC Playtime

Mini-Overlay im Star-Citizen-HUD-Stil, das die Spielzeit erfasst. Eigenständiges Tool,
kein Bezug zu anderen Projekten.

📖 **[Hilfe – alle Funktionen erklärt](HILFE.md)** · 📝 **[Changelog](CHANGELOG.md)**

- erkennt `StarCitizen.exe` automatisch (alle 2 s, nur Prozessliste lesen)
- **Channel aus dem Installationsordner**: `…\StarCitizen\LIVE\Bin64\StarCitizen.exe` → LIVE,
  ebenso PTU, EPTU, HOTFIX, TECH-PREVIEW — getrennt auswertbar oder zusammen („ALLE“)
- **mehrere Spiele**: beliebige weitere EXEs über Rechtsklick → Spiel → Spiel hinzufügen …
- Anzeige: laufende Session (große Uhr), Heute / Woche; aufgeklappt: Monat, Jahr, Gesamt,
  Serie (Tage am Stück), Sessions, Ø- und längste Session, Balkendiagramm
  Tag (14) / Woche (12) / Monat (12) / Jahr (5) mit Hover-Werten
- Transparenz: Hintergrund und Gesamt-Deckkraft getrennt per Schieberegler
- Farben: Statistik-Kacheln werden im Spiel eingefärbt (Standard Grün mit dunkler Schrift),
  Kacheln und aktiver Channel-Chip per Vorlage oder freier Farbwahl einstellbar
- Autostart mit Windows (HKCU\…\Run, kein Admin), Tray-Icon, Einzelinstanz

## Start

```powershell
cd sc-playtime
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pythonw.exe run.pyw
```

Der Autostart-Eintrag (Rechtsklick → „Mit Windows starten“) merkt sich genau diesen
Python-Interpreter und `run.pyw`. Wird der Ordner verschoben, einmal aus- und wieder
einschalten.

## Bedienung

| Aktion | |
| --- | --- |
| Klick auf den Kopf | Statistik auf-/zuklappen |
| Ziehen | Overlay verschieben (sperrbar) |
| Klick auf Chip / Tab | Channel-Filter bzw. Zeitraum |
| Rechtsklick / Tray-Icon | Menü: Spiel, Transparenz, Autostart, … |
| Klick auf Tray-Icon | Overlay ein-/ausblenden |

„Klicks durchlassen“ macht das Overlay für die Maus unsichtbar — zurückschalten dann
über das Tray-Icon.

Star Citizen muss im **Fenstermodus randlos** laufen, sonst kann kein Overlay darüber
gezeichnet werden (gilt für alle Overlays).

## Daten

`%APPDATA%\SC-Playtime\`

- `playtime.db` — SQLite, Tabelle `sessions(game, channel, start, end)`
- `settings.json` — Position, Transparenz, Spieleliste …

Das Session-Ende wird alle 30 s gesichert; läuft das Spiel beim Start des Overlays
bereits, zählt die Session ab dem echten Prozessstart.

## EXE bauen

```powershell
.venv\Scripts\pip install pyinstaller
.venv\Scripts\python.exe build.py
```

Ergebnis: `dist\SC-Playtime.exe` (eine Datei, ohne Konsole). Wird der Autostart aus der
EXE heraus eingeschaltet, zeigt der Eintrag auf die EXE.

## Tests

```powershell
python -m unittest discover -s tests
```
