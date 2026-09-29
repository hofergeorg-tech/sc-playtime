# Changelog

Alle nennenswerten Änderungen an SC Playtime. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## [1.1.0] – 2026-09-29

### Neu
- **Farben einstellbar** (Menü → Farben):
  - *Statistik-Kacheln (im Spiel)*: Vorlagen Grün, Cyan, Bernstein oder „Nicht
    einfärben“ sowie freie Wahl von Hintergrund- und Schriftfarbe.
  - *Aktiver Channel*: Vorlagen für den ausgewählten Channel-Chip sowie freie Farbwahl.
- Statistik-Kacheln werden bei laufendem Spiel eingefärbt (Standard: Grün mit dunkler
  Schrift). Offline bleiben sie dunkel im HUD-Stil.
- Hilfe (`HILFE.md`) mit Beschreibung aller Funktionen.

### Behoben
- Bei laufendem Spiel wurden Kacheln und Channel-Chips versehentlich hellgrün gefüllt,
  die weiße Schrift darauf war kaum lesbar. Ursache war die Füllfarbe des Status-Punkts,
  die danach aktiv blieb.

## [1.0.0] – 2026-09-28

Erste Version.

### Neu
- Rahmenloses Overlay im Star-Citizen-HUD-Stil, immer im Vordergrund.
- Automatische Erkennung von `StarCitizen.exe` (Prozessliste, alle 2 s, nur lesend).
- Channel-Erkennung aus dem Installationsordner: LIVE, PTU, EPTU, HOTFIX, TECH-PREVIEW;
  Statistik je Channel oder gesamt.
- Mehrere Spiele: beliebige EXEs hinzufügen und entfernen.
- Kompakte Ansicht: Session-Uhr, Heute, Woche.
- Aufgeklappte Statistik: Kacheln (Heute, Woche, Monat, Jahr, Gesamt, Serie),
  Balkendiagramm Tag / Woche / Monat / Jahr / Gesamt mit Hover-Werten,
  Sessions, Ø- und längste Session.
- Transparenz für Hintergrund und Gesamt getrennt einstellbar.
- Position sperren, Klicks durchlassen, nur anzeigen wenn ein Spiel läuft.
- Tray-Icon, Einzelinstanz, Autostart mit Windows (ohne Admin).
- Speicherung in SQLite unter `%APPDATA%\SC-Playtime\`; Session-Ende alle 30 s gesichert.
- Build einer einzelnen EXE per PyInstaller (`build.py`).
