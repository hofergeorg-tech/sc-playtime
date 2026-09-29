# SC Playtime – Hilfe

🇬🇧 [English version](HELP.md)

SC Playtime ist ein kleines Overlay, das mitzählt, wie lange du Star Citizen (oder andere
Spiele) spielst. Es sitzt als schmales Panel über dem Spiel und zeigt die laufende
Session sowie deine Statistik. Es läuft unter **Windows** und **Linux**.

- [Installation und Start](#installation-und-start)
- [Das Overlay](#das-overlay)
- [Bedienung mit der Maus](#bedienung-mit-der-maus)
- [Das Menü](#das-menü)
- [Farben](#farben)
- [Sprache](#sprache)
- [Mehrere Spiele](#mehrere-spiele)
- [Channels (LIVE, PTU, …)](#channels-live-ptu-)
- [So wird gezählt](#so-wird-gezählt)
- [Updates](#updates)
- [Linux](#linux)
- [Deine Daten](#deine-daten)
- [Häufige Fragen](#häufige-fragen)

---

## Installation und Start

**Windows:** `SC-Playtime.exe` von der
[Release-Seite](https://github.com/hofergeorg-tech/sc-playtime/releases/latest) laden,
in einen eigenen Ordner legen (z. B. `Dokumente\SC-Playtime`) und starten. Keine
Installation nötig; das Tray-Icon (Uhr im Rahmen) erscheint unten rechts in der
Taskleiste.

**Linux:** siehe [Linux](#linux).

**Aus dem Quellcode (Windows):**

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pythonw.exe run.pyw
```

Es läuft immer nur eine Instanz. Ein zweiter Start (z. B. Autostart plus manueller
Start) beendet sich sofort wieder, damit nichts doppelt gezählt wird.

> **Wichtig:** Star Citizen muss im Modus **„Fenster (randlos)“** laufen. Im echten
> Vollbild kann kein Overlay darüber gezeichnet werden – das gilt für alle Overlays.

## Das Overlay

### Kompakte Ansicht

| Bereich | Bedeutung |
| --- | --- |
| Punkt oben links | pulsiert grün, solange das Spiel läuft; grau, wenn offline |
| Spielname | das angezeigte Spiel, daneben der Channel (z. B. **LIVE**) |
| **IM SPIEL** / **OFFLINE** | Status oben rechts |
| große Uhr | Dauer der laufenden Session; offline die Dauer der letzten Session |
| HEUTE / WOCHE | heute gespielt bzw. seit Montag dieser Woche |

### Aufgeklappte Statistik

Ein Klick auf den Kopf des Overlays klappt die Statistik auf bzw. zu.

- **Channel-Filter** (ALLE, LIVE, PTU, …): zeigt die Statistik nur für einen Channel oder
  für alle zusammen. Erscheint, sobald Sessions mit Channel erfasst wurden.
- **Kacheln:**

  | Kachel | Bedeutung |
  | --- | --- |
  | HEUTE | Spielzeit seit Mitternacht |
  | WOCHE | seit Montag 0:00 Uhr |
  | MONAT | seit dem 1. des Monats |
  | JAHR | seit dem 1. Januar |
  | GESAMT | alles, was je erfasst wurde |
  | SERIE | Tage am Stück mit mindestens 1 Minute Spielzeit. Heute noch nicht gespielt unterbricht die Serie nicht. |

- **Diagramm** mit den Reitern:

  | Reiter | zeigt |
  | --- | --- |
  | TAG | die letzten 14 Tage |
  | WOCHE | die letzten 12 Kalenderwochen |
  | MONAT | die letzten 12 Monate |
  | JAHR | die letzten 5 Jahre |
  | GESAMT | jedes Jahr seit deiner ersten Session |

  Der aktuelle Zeitraum ist grün hervorgehoben. Fährst du mit der Maus über einen
  Balken, steht unten der genaue Zeitraum und die Spielzeit.

  Ist ein Channel-Filter aktiv (z. B. PTU), zeigen die farbigen Balken nur diesen
  Channel. Dahinter steht grau die Gesamtzeit aller Channels, und die Skala bleibt die
  gleiche wie bei „ALLE“ – so ist sofort sichtbar, welcher Anteil auf den Channel
  entfällt. Beim Überfahren steht unten z. B. „PTU 6m / 11h 31m“.
- **Fußzeile:** Anzahl Sessions, durchschnittliche und längste Session (Sessions unter
  1 Minute werden hier nicht mitgezählt).

## Bedienung mit der Maus

| Aktion | Wirkung |
| --- | --- |
| Klick auf den Kopf | Statistik auf-/zuklappen |
| Ziehen mit gedrückter linker Maustaste | Overlay verschieben (außer „Position sperren“ ist an) |
| Klick auf einen Channel-Chip | Channel-Filter setzen |
| Klick auf einen Reiter | Zeitraum des Diagramms wechseln |
| Maus über einem Balken | genaue Werte in der Fußzeile |
| Rechtsklick aufs Overlay | Menü |
| Linksklick aufs Tray-Icon | Overlay ein-/ausblenden |
| Rechtsklick aufs Tray-Icon | Menü (auch wenn das Overlay ausgeblendet ist) |

Position, aufgeklappter Zustand, gewählter Reiter und Filter werden gespeichert und beim
nächsten Start wiederhergestellt.

## Das Menü

| Eintrag | Funktion |
| --- | --- |
| Overlay ein-/ausblenden | nur im Tray-Menü |
| Statistik aufgeklappt | wie Klick auf den Kopf |
| Spiel | angezeigtes Spiel wählen, Spiele hinzufügen oder entfernen |
| HINTERGRUND (Schieberegler) | Deckkraft nur des dunklen Hintergrunds; Schrift bleibt voll sichtbar |
| DECKKRAFT GESAMT (Schieberegler) | Deckkraft des ganzen Overlays (20–100 %) |
| Farben | siehe [Farben](#farben) |
| Sprache | siehe [Sprache](#sprache) |
| Position sperren | Overlay lässt sich nicht mehr verschieben |
| Klicks durchlassen | Mausklicks gehen durch das Overlay ins Spiel. Ausschalten nur noch über das **Tray-Icon** möglich. |
| Nur anzeigen, wenn ein Spiel läuft | Overlay blendet sich offline automatisch aus |
| Mit Windows starten / Beim Anmelden starten | Autostart beim Anmelden (ohne Admin-Rechte) |
| Hilfe … | diese Hilfe |
| Was ist neu? … | Changelog mit allen Änderungen je Version |
| Nach Updates suchen | sofort bei GitHub nachsehen, siehe [Updates](#updates) |
| Automatisch nach Updates suchen | beim Start und alle 12 Stunden prüfen (Standard: an) |
| ⬆ Update auf … installieren | erscheint ganz oben, wenn eine neue Version bereitliegt |
| Datenordner öffnen | öffnet den Ordner mit Datenbank und Einstellungen |
| Beenden | Overlay schließen; die laufende Session wird vorher gesichert |

## Farben

Unter **Menü → Farben** gibt es zwei Bereiche. Jeder hat Vorlagen sowie
„Hintergrundfarbe wählen …“ und „Schriftfarbe wählen …“ für eigene Farben.

**Statistik-Kacheln (im Spiel)** – offline sind die Kacheln immer dunkel im HUD-Stil.
Sobald das Spiel läuft, werden sie eingefärbt:

- Grün / Dunkel (Standard)
- Cyan / Dunkel
- Bernstein / Dunkel
- Nicht einfärben (HUD) – Kacheln bleiben auch im Spiel dunkel

**Aktiver Channel** – der ausgewählte Channel-Chip (im Kopf und im Filter):

- Automatisch – Farbe des Channels (LIVE grün, PTU gelb, …) mit dunkler Schrift
- Dunkelgrün / Weiß, Schwarz / Grün, Dunkelblau / Weiß, Weiß / Schwarz

Tipp: Für gute Lesbarkeit helle Hintergründe mit dunkler Schrift kombinieren und
umgekehrt.

## Sprache

Unter **Menü → Sprache** (mit Flagge) stehen zur Wahl:

- **Automatisch (System)** – Standard; Deutsch, wenn das Betriebssystem auf Deutsch
  steht, sonst Englisch
- 🇩🇪 **Deutsch**
- 🇬🇧 **English**

Die Umstellung wirkt sofort auf Overlay, Menü, Meldungen, Hilfe und „Was ist neu?“.

## Mehrere Spiele

Standardmäßig wird `StarCitizen.exe` verfolgt. Weitere Spiele:

1. Rechtsklick → **Spiel → Spiel hinzufügen …**
2. Das Programm des Spiels auswählen (Windows: die `.exe`; Linux: siehe unten).
3. Einen Anzeigenamen vergeben.

Erkannt wird das Spiel am Programmnamen. Läuft ein Spiel, zeigt das Overlay automatisch
dieses an; laufen mehrere, das im Menü gewählte. Über **Spiel entfernen** wird ein
Spiel nicht mehr verfolgt – seine bisherigen Sessions bleiben gespeichert.

## Channels (LIVE, PTU, …)

Der Channel wird aus dem Installationsordner gelesen:

```
…\StarCitizen\LIVE\Bin64\StarCitizen.exe   →  LIVE
…\StarCitizen\PTU\Bin64\StarCitizen.exe    →  PTU
```

Ebenso EPTU, HOTFIX und TECH-PREVIEW. Jede Session merkt sich ihren Channel, so lässt
sich die Statistik getrennt oder gesamt („ALLE“) anzeigen.

## So wird gezählt

- Alle 2 Sekunden wird die Prozessliste gelesen. Es wird nur **gelesen** – nichts wird
  ins Spiel eingeschleust.
- Startest du das Overlay erst, wenn das Spiel schon läuft, zählt die Session trotzdem
  ab dem echten Start des Spiels.
- Das Session-Ende wird alle 30 Sekunden gespeichert. Stürzt der PC ab, fehlen
  höchstens diese 30 Sekunden.
- Sessions über Mitternacht (oder über Wochen-/Monatsgrenzen) werden anteilig auf die
  Zeiträume verteilt.

## Updates

Die aktuelle Version steht oben im Menü (z. B. „SC PLAYTIME 1.3.0“).

- **Automatisch:** Ist „Automatisch nach Updates suchen“ an, schaut SC Playtime kurz nach
  dem Start und danach alle 12 Stunden auf GitHub nach einer neuen Version. Gibt es eine,
  erscheint eine Meldung am Tray-Icon und oben im Menü der Eintrag
  **„⬆ Update auf … installieren“**.
- **Von Hand:** Menü → „Nach Updates suchen“.
- **Installieren:** Nach der Bestätigung wird die neue Version heruntergeladen. Das
  Overlay speichert die laufende Session, beendet sich, ersetzt die Programmdatei und
  startet neu. Danach wird einmal „Was ist neu?“ angezeigt. Einstellungen und
  Spielzeiten bleiben erhalten.
- Läuft SC Playtime aus dem Quellcode statt als fertiges Programm, öffnet
  „Installieren“ stattdessen die Release-Seite im Browser.

Alle Versionen gibt es auch unter
<https://github.com/hofergeorg-tech/sc-playtime/releases>.

## Linux

**Fertiges Programm:** `SC-Playtime-linux-x86_64` von der
[Release-Seite](https://github.com/hofergeorg-tech/sc-playtime/releases/latest) laden,
z. B. nach `~/Programme/` legen, ausführbar machen und starten:

```bash
chmod +x SC-Playtime-linux-x86_64
./SC-Playtime-linux-x86_64
```

**Aus dem Quellcode:**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.pyw
```

Hinweise:

- **Star Citizen unter Wine/Proton/Lutris** wird wie unter Windows erkannt – auch der
  Channel (LIVE, PTU, …), weil der Windows-Pfad des Spiels mitgelesen wird.
- **Native Linux-Spiele** über „Spiel hinzufügen …“ mit dem Programm des Spiels anlegen
  (Dateifilter auf „Alle Dateien“ stellen). Erkannt wird der Programmname.
- **Wayland:** Unter Wayland dürfen Fenster weder ihre Position festlegen noch immer im
  Vordergrund bleiben. SC Playtime startet deshalb automatisch über **XWayland**, das auf
  fast allen Desktops vorhanden ist. Wer es anders will, setzt `QT_QPA_PLATFORM` selbst.
- **Tray-Icon unter GNOME:** GNOME zeigt Tray-Icons erst mit der Erweiterung
  „AppIndicator and KStatusNotifierItem Support“. KDE, XFCE, Cinnamon & Co. brauchen
  nichts.
- **Autostart** heißt im Menü „Beim Anmelden starten“ und legt
  `~/.config/autostart/sc-playtime.desktop` an.
- **Daten** liegen unter `~/.local/share/SC-Playtime/`.

## Deine Daten

Alles liegt lokal (Menü → „Datenordner öffnen“):

- Windows: `%APPDATA%\SC-Playtime\`
- Linux: `~/.local/share/SC-Playtime/`

| Datei | Inhalt |
| --- | --- |
| `playtime.db` | SQLite-Datenbank mit allen Sessions (Spiel, Channel, Start, Ende) |
| `settings.json` | Position, Transparenz, Farben, Sprache, Spieleliste, … |

Deine Spielzeiten und Einstellungen verlassen nie deinen PC. Die einzige Verbindung ins
Internet ist die Update-Prüfung: Sie ruft nur die öffentliche Versionsinfo bei GitHub ab
und lässt sich im Menü abschalten. Zum Sichern oder Umziehen einfach den Ordner kopieren.
Zum Zurücksetzen der Einstellungen `settings.json` bei beendetem Overlay löschen.

## Häufige Fragen

**Das Overlay ist im Spiel nicht zu sehen.**
Star Citizen auf „Fenster (randlos)“ stellen. Prüfen, ob das Overlay über das Tray-Icon
ausgeblendet wurde.

**Ich kann das Overlay nicht mehr anklicken.**
„Klicks durchlassen“ ist an. Rechtsklick aufs Tray-Icon und den Haken entfernen.

**Das Overlay ist verschwunden.**
Linksklick aufs Tray-Icon blendet es wieder ein. Ist „Nur anzeigen, wenn ein Spiel
läuft“ aktiv, erscheint es offline nicht.

**Der Autostart funktioniert nicht mehr.**
Der Eintrag zeigt auf den Ort des Programms bzw. von `run.pyw`. Nach dem Verschieben
des Ordners den Autostart im Menü einmal aus- und wieder einschalten.

**Das Update schlägt fehl.**
Prüfen, ob Internet da ist, und es mit „Nach Updates suchen“ erneut versuchen. Liegt
das Programm in einem geschützten Ordner (z. B. `C:\Programme` oder `/usr/bin`), kann es
sich nicht selbst ersetzen – dann die neue Version von der Release-Seite laden oder das
Programm in einen eigenen Ordner legen.

**Windows meldet „Der Computer wurde durch Windows geschützt“.**
Die EXE ist noch nicht digital signiert (beantragt, siehe
[CODE_SIGNING.md](CODE_SIGNING.md)), deshalb warnt SmartScreen bei neuen Downloads. Auf
„Weitere Informationen“ → „Trotzdem ausführen“ klicken. Wer prüfen will, dass die Datei
wirklich aus diesem Repository gebaut wurde:
`gh attestation verify SC-Playtime.exe --repo hofergeorg-tech/sc-playtime`

**Stört das den Anti-Cheat?**
SC Playtime liest nur die Prozessliste und die Startzeit des Spiels über normale
Funktionen des Betriebssystems, so wie der Task-Manager. Es greift nicht auf das Spiel
zu.
