# Changelog

🇬🇧 [English](CHANGELOG.en.md) · 🇫🇷 [Français](CHANGELOG.fr.md) · 🇪🇸 [Español](CHANGELOG.es.md) · 🇮🇹 [Italiano](CHANGELOG.it.md) · 🇵🇱 [Polski](CHANGELOG.pl.md) · 🇨🇳 [简体中文](CHANGELOG.zh.md)

Alle nennenswerten Änderungen an SC Playtime. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## [1.6.0] – 2026-10-17

### Neu
- **Anti-AFK** (Windows): Menü → Anti-AFK hält Star Citizen wach. Drückt im Takt die Taste
  rechts neben P (Ü/[, Standard alle 5 s) und/oder bewegt die Maus in einem kleinen Muster
  (Rechts–links, Hoch–runter, Quadrat, Kreis, zufällig; Weite, Tempo und Takt einstellbar).
  Gesendet werden echte Scancodes – nur, wenn das Spiel im Vordergrund ist. Ein/aus per Menü
  oder **Strg+Umschalt+F12**; Ringe neben der Uhr zeigen den Takt und schalten die Aktion per
  Klick. Die eigenen Eingaben zählen nicht für die AFK-Erkennung.

## [1.5.0] – 2026-10-09

### Neu
- **Abstürze und Server-Abbrüche je Patch:** SC Playtime liest nach dem Spielende das
  `Game.log` von Star Citizen und merkt sich, ob du selbst beendet hast, das Spiel
  abgestürzt ist oder der Server die Verbindung getrennt hat. Die Auswertung zeigt je Patch
  Abstürze (z. B. „2 · alle 6h 30m“) und Server-Abbrüche, das Sessions-Fenster eine Spalte
  „Ausgang“. Ältere Sessions werden beim Start aus den gesicherten Logs (`logbackups`)
  nachträglich eingeordnet.
- **Tagesverlauf** in der Auswertung: ein Tag als Zeitstrahl von 0 bis 24 Uhr mit allen
  Sessions in Channel-Farbe, Pausen als Lücken, Absturz (rot) und Server-Abbruch (gelb) als
  Marke; mit ‹ › zwischen den Spieltagen blättern.
- **Zwei PCs zusammenführen:** Menü → Daten → „Sessions eines anderen PCs übernehmen …“
  holt die Spielzeit aus der `playtime.db` (oder einer Sicherung) eines anderen PCs dazu.
  Schon vorhandene Sessions werden erkannt und übersprungen, vorher wird gesichert.
- **Seit wann gezählt wird:** Die GESAMT-Kachel zeigt oben rechts das Datum der ersten
  Aufzeichnung.
- **Hilfe und Changelog in allen sieben Sprachen** (bisher nur Deutsch und Englisch).

### Geändert
- Der CSV/JSON-Export enthält eine Spalte `ending` (`quit`, `crash`, `server`).

## [1.4.1] – 2026-10-09

### Verbessert
- **Schnelleres Overlay bei langer Spielhistorie:** Die Statistik wurde jede Sekunde komplett
  neu berechnet, und der Aufwand wuchs quadratisch mit der Zahl der Sessions (bei 5000
  Sessions 1,5 s – jede Sekunde, über dem Spiel). Jetzt werden abgeschlossene Sessions nur
  einmal ausgewertet und pro Sekunde nur die laufende ergänzt: 2 ms statt 1500 ms.
- Der pulsierende Punkt zeichnet das Overlay nur noch 8- statt 16-mal pro Sekunde neu.

### Sicherheit
- Updates werden nur installiert, wenn die heruntergeladene Datei zur Prüfsumme passt, die
  GitHub für das Release angibt.
- Einstellungen werden zuerst vollständig in eine Zwischendatei geschrieben und dann
  getauscht – ein Absturz beim Speichern setzt sie nicht mehr auf Standard zurück.

## [1.4.0] – 2026-10-04

### Neu
- **Diagramm zurückblättern:** Bei TAG, WOCHE und MONAT blättern die Pfeile ‹ › oben
  rechts am Diagramm in die Vergangenheit, das Mausrad schrittweise – bis zur ersten
  Session.
- **Auswertung** (Menü → Auswertung …): Heatmap „Wann spielst du?“ nach Wochentag und
  Uhrzeit sowie **Spielzeit je Patch**. Die Star-Citizen-Version (z. B. 4.3.1) wird ab
  jetzt bei jeder Session aus dem Installationsordner gelesen und gespeichert.
- **Sessions bearbeiten** (Menü → Sessions bearbeiten …): Start und Ende korrigieren
  oder Sessions löschen, z. B. nach Standby mit offenem Spiel.
- **AFK-Erkennung** (Menü → AFK-Erkennung): optional nach 5–30 Minuten ohne Eingabe
  pausieren; die Session endet beim letzten Tastendruck, bei der nächsten Eingabe
  beginnt eine neue. Das Overlay zeigt dann „AFK“.
- **Globale Tastenkürzel** (Windows): Strg+Umschalt+F9 blendet das Overlay ein/aus,
  Strg+Umschalt+F11 schaltet „Klicks durchlassen“ um – auch im Spiel. Änderbar unter
  Menü → Tastenkürzel ….
- **Export** aller Sessions als CSV (für Excel) oder JSON (Menü → Daten).
- **Automatische Sicherung:** einmal täglich eine Kopie der Datenbank in `backups`, die
  letzten 7 bleiben liegen; zusätzlich „Jetzt sichern“ im Menü.
- **Neue Sprachen:** Français, Español, Italiano, Polski und 简体中文 (Hilfe und
  Changelog dort auf Englisch).
- **Über SC Playtime** im Menü mit Version, Links und Spenden-Knopf (PayPal).

### Behoben
- Das Kontextmenü (und Farbwähler oder Meldungen) verschwand oft hinter dem Overlay
  bzw. hinter dem Spiel. Menüs und Dialoge liegen jetzt immer obenauf, und das Overlay
  drängt sich nicht mehr davor, solange eines offen ist.

## [1.3.2] – 2026-09-29

### Behoben
- **Diagramm mit Channel-Filter:** Mit z. B. PTU sah das Diagramm genauso aus wie mit
  ALLE, weil es sich immer auf den eigenen größten Balken skalierte – 6 Minuten PTU
  füllten die Höhe genauso wie 11 Stunden gesamt. Jetzt bleibt die Skala die von ALLE,
  die Gesamtzeit steht grau dahinter, der gewählte Channel wird in seiner Farbe davor
  gezeichnet. Beim Überfahren: „PTU 6m / 11h 31m“.

## [1.3.1] – 2026-09-29

### Neu
- **Herkunftsnachweis:** Jede Release-Datei ist per GitHub-Attestation überprüfbar
  (`gh attestation verify …`). Die Windows-Signatur über SignPath Foundation ist
  beantragt und im Build vorbereitet.
- Lizenz: MIT.
- Hilfe: Abschnitt zur SmartScreen-Warnung.

## [1.3.0] – 2026-09-29

### Neu
- **Englisch als Sprache:** Menü → Sprache mit Flaggen (🇩🇪 Deutsch, 🇬🇧 English)
  oder „Automatisch“ nach Systemsprache. Overlay, Menü, Meldungen, Hilfe und
  Changelog sind vollständig übersetzt; weitere Sprachen lassen sich leicht ergänzen.
- **Linux-Unterstützung:** Prozess-Erkennung über `/proc` (auch Star Citizen unter
  Wine/Proton/Lutris inklusive Channel), Autostart über `~/.config/autostart`,
  Daten unter `~/.local/share/SC-Playtime`, automatischer Start über XWayland.
  Fertiges Programm `SC-Playtime-linux-x86_64` im Release, Selbst-Update auch unter Linux.
- Automatische Builds und Tests für Windows und Linux über GitHub Actions.

### Behoben
- Meldungsfenster (z. B. „Kein Update“) zeigten dunkle Schrift auf dunklem Grund und
  wirkten leer.

## [1.2.0] – 2026-09-29

### Neu
- **Update-Funktion:** prüft beim Start und alle 12 Stunden, ob es auf GitHub eine
  neue Version gibt. Ist eine da, erscheint eine Meldung am Tray-Icon und oben im Menü
  „Update installieren“. Die EXE lädt die neue Version herunter, ersetzt sich selbst und
  startet neu – die laufende Session wird vorher gespeichert.
- Menü: **Nach Updates suchen** und **Automatisch nach Updates suchen** (abschaltbar).
- Menü: **Hilfe** und **Was ist neu?** öffnen Hilfe und Changelog direkt im Programm,
  auch ohne Internet.
- Nach einem Update wird „Was ist neu?“ einmal automatisch angezeigt.
- Versionsnummer im Menütitel und in den Fenstern.

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
