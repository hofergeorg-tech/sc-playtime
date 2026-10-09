# Security- & Performance-Review — sc-playtime

**Datum:** 2026-10-09
**Reviewer:** Claude (Opus 5.5)
**Stand:** v1.4.0 (`c6261af`)
**Umfang:** Statische Durchsicht von `sc_playtime/` (Python 3.13, PySide6), `build.py`,
`.github/workflows/ci.yml`; Messung der Overlay-Neuberechnung mit synthetischen Daten.

> **Status (2026-10-09, v1.4.1):** P1, P2, P3 und S1 behoben; S2/S3 offen (Info, S3 wartet auf SignPath).
>
> | Befund | Status |
> |---|---|
> | P1 | ✅ Tagessummen in einem Durchgang (`stats.daily_totals`), Balken/Serie/Zeiträume daraus; abgeschlossene Sessions im Overlay zwischengespeichert (`Tracker.revision`), pro Sekunde nur die laufende Session. Messung: 5000 Sessions 1500 ms → 2,3 ms pro Sekunde (+ 13 ms einmalig, wenn eine Session endet). Test vergleicht die Zahlen mit der alten Berechnung. |
> | P2 | ✅ Puls 125 ms statt 60 ms |
> | P3 | ✅ `settings.json` über `.tmp` + `os.replace` |
> | S1 | ✅ SHA-256 aus dem GitHub-`digest` wird nach dem Download geprüft |

---

## Zusammenfassung

| # | Befund | Schweregrad | Ort |
|---|--------|-------------|-----|
| P1 | Overlay rechnet jede Sekunde die komplette Statistik neu – Aufwand wächst quadratisch mit der Spielhistorie | **Mittel (wächst)** | `ui.py:314` (`refresh`), `stats.py:148` (`summarize`) |
| P2 | Puls-Animation zeichnet das Overlay ~16× pro Sekunde über dem Spiel neu | Niedrig | `ui.py:296` |
| P3 | `settings.json` wird nicht atomar geschrieben (Absturz beim Speichern → alle Einstellungen weg) | Niedrig | `settings.py:66` |
| S1 | Selbst-Update ohne Prüfsumme (nur Mindestgröße 1 MB) | Niedrig/Mittel | `updater.py:73` |
| S2 | CI-Actions per Versions-Tag statt Commit-Hash eingebunden | Info | `ci.yml` |
| S3 | EXE unsigniert (SignPath vorbereitet, Freigabe ausstehend) | Info | `ci.yml:73` |

Positiv: Keine Adminrechte, Autostart nur über `HKCU\…\Run`. Prozesse werden nur gelesen
(`PROCESS_QUERY_LIMITED_INFORMATION`, Toolhelp-Snapshot) – nichts greift ins Spiel ein, also
unbedenklich für Anti-Cheat. Netz nur zu GitHub, im Hintergrund-Thread, ohne Nutzerdaten.
Globale Tastenkürzel in eigenem Thread mit Nachrichtenschleife (blockiert die Oberfläche nicht).
SQLite ausschließlich mit Parametern; Sicherung atomar (`.tmp` → `replace`, SQLite-Backup-API).
Einzelinstanz-Sperre verhindert doppeltes Zählen. Links in Hilfe/Changelog nur `http/https`.
Build-Herkunftsnachweis (Sigstore-Attestation) im CI.

---

## P1 — Neuberechnung jede Sekunde, quadratischer Aufwand  ⚠️ Mittel (wächst mit der Zeit)

**Ort:** `ui.py:294` (`_tick` alle 1000 ms → `refresh()`), `stats.py:148` (`summarize`)

`refresh()` holt jede Sekunde alle Sessions des Spiels (neue Listen-Kopie), berechnet die
Zusammenfassung, 14–12 Balken und noch einmal die Gesamt-Balken. Teuer ist die **Serie**
(„Tage in Folge“): Für jeden Tag der Serie läuft `played()` über **alle** Sessions →
Aufwand ≈ Serienlänge × Sessions, jede Sekunde, im GUI-Thread, über dem laufenden Spiel.

Messung (synthetisch, ein Kern, Python 3.13):

| Sessions | Zeit pro `refresh` |
|---:|---:|
| 50 | 2 ms |
| 500 | 19 ms |
| 2000 | 264 ms |
| 5000 | 1500 ms |

Heutiger Stand beim Nutzer: 43 Sessions in 11 Tagen (≈ 4 pro Spieltag) → unkritisch. Nach
einem Jahr regelmäßigen Spielens (> 1000 Sessions, AFK-Erkennung teilt Abende zusätzlich)
wird das Overlay spürbar träge und kostet dauerhaft CPU; ab einigen tausend Sessions blockiert
es sich praktisch selbst.

**Behebung:** Tagessummen einmal in einem Durchgang bilden (Dictionary Tag → Sekunden), Serie
und Balken daraus ablesen (linear statt quadratisch). Außerdem abgeschlossene Sessions cachen:
Pro Sekunde ändert sich nur das Ende der laufenden Session – nur deren Anteil neu rechnen, den
Rest erst bei neuer/geänderter Session. Erwartung: < 5 ms auch bei 5000 Sessions.

## P2 — Puls-Animation mit ~16 Hz  Niedrig

**Ort:** `ui.py:296` (`_pulse`, 60 ms)

Solange ein Spiel läuft, wird der Puls-Punkt alle 60 ms neu gezeichnet. Das Overlay ist ein
durchscheinendes Fenster über dem Spiel; jede Aktualisierung lässt Windows (DWM) das Fenster
neu zusammensetzen. Einzeln billig, aber dauerhaft während des Spielens.

**Behebung:** Takt auf ~250 ms senken (sieht kaum anders aus) oder Puls im Klick-durch-Modus /
bei verstecktem Overlay ganz aussetzen (Letzteres passiert schon über `isVisible`).

## P3 — Einstellungen nicht atomar gespeichert  Niedrig

**Ort:** `settings.py:66` (`path.write_text(...)`)

Stürzt die App oder Windows genau beim Schreiben ab, ist `settings.json` halb geschrieben;
`Settings.load` fängt den Fehler und startet **still mit Standardwerten** – Spieleliste,
Position, Farben, Hotkeys sind weg (die Spielzeit selbst liegt sicher in der DB).

**Behebung:** In `settings.json.tmp` schreiben und mit `os.replace` tauschen (wie schon bei
der Sicherung).

## S1 — Selbst-Update ohne Prüfsumme  Niedrig/Mittel

**Ort:** `updater.py:73` (`download`), `update_ui.py:118`

Die neue EXE wird nur auf Mindestgröße geprüft und dann per Batch an die Stelle der alten
gesetzt und gestartet. Schutz hängt allein an TLS + dem GitHub-Konto. Die GitHub-API liefert
zu jeder Release-Datei einen `digest` (`sha256:…`).

**Behebung:** `digest` in `fetch_latest` mitlesen, nach dem Download SHA-256 vergleichen,
bei Abweichung verwerfen (wie in NoFences 2.13). Volle Absicherung später über die Signatur (S3).

## S2 — CI-Actions per Tag  Info

`actions/checkout@v4`, `signpath/…@v1` usw. zeigen auf verschiebbare Tags. Wird ein
Action-Repo kompromittiert, läuft fremder Code im Release-Build (mit `contents: write`).
Härtung: auf Commit-SHAs pinnen (`uses: actions/checkout@<sha> # v4`), Dependabot hält sie aktuell.

## S3 — Unsigniert  Info

Signatur über SignPath Foundation ist im CI vorbereitet; es fehlen `SIGNPATH_API_TOKEN` und
`SIGNPATH_ORGANIZATION_ID` (Freigabe ausstehend). Bis dahin SmartScreen-Warnung.

---

## Nicht als Problem bestätigt (geprüft)

- **Prozesszugriff:** nur lesend, kein Debug-/VM-Recht, kein Einhaken ins Spiel.
- **Netz:** nur `api.github.com` / Release-Download, Timeouts gesetzt, Hintergrund-Thread.
- **Release-Notes** im Update-Dialog als reiner Text (kein HTML/Markdown-Rendering).
- **Update-Batch** in `%TEMP%` (nutzereigen), Pfade in Anführungszeichen; Rechte bleiben beim Nutzer.
- **CSV-Export:** enthält nur eigene Daten; Formel-Injection über Spielnamen theoretisch, aber
  ohne fremde Eingabe irrelevant.
- **Daten:** `%APPDATA%\SC-Playtime` (nur für den Nutzer), tägliche Sicherung mit 7 Ständen.

## Empfohlene Reihenfolge

1. **P1** – linear rechnen + Cache (größte Wirkung auf Dauer).
2. **S1** – Prüfsumme beim Update (klein, wie bei NoFences).
3. **P3** – atomar speichern (eine Zeile).
4. **P2** – Puls langsamer.
5. S2/S3 nach Bedarf (S3 wartet auf SignPath).
