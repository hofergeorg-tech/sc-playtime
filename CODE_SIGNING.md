# Code signing policy

🇩🇪 Deutsche Einrichtungsanleitung weiter unten.

## Status

Windows builds are **not yet Authenticode-signed**. Free code signing via
[SignPath Foundation](https://signpath.org) has been requested. Once approved, this
section will read:

> Free code signing provided by [SignPath.io](https://signpath.io), certificate by
> [SignPath Foundation](https://signpath.org).

Until then, every release file carries a **build provenance attestation**, which proves
that it was built by GitHub Actions from this repository:

```bash
gh attestation verify SC-Playtime.exe --repo hofergeorg-tech/sc-playtime
```

## What gets signed

Only `SC-Playtime.exe` from the [releases](https://github.com/hofergeorg-tech/sc-playtime/releases),
built by the [CI workflow](.github/workflows/ci.yml) from a version tag. Nothing is
signed on a developer machine.

## Team roles

| Role | Members |
| --- | --- |
| Committers and reviewers | [hofergeorg-tech](https://github.com/hofergeorg-tech) |
| Approvers | [hofergeorg-tech](https://github.com/hofergeorg-tech) |

## Privacy policy

SC Playtime does not transfer any personal information to other networked systems.
Playtimes and settings stay on the local computer. The only network access is the
optional update check, which requests the public release information from
`api.github.com` (and, when the user confirms an update, downloads the release file from
`github.com`). It can be turned off in the menu ("Check for updates automatically").

---

## Einrichtung (für den Maintainer)

Die Signatur läuft vollständig in GitHub Actions. Der Workflow ist schon vorbereitet und
signiert automatisch, sobald die zwei Werte unten gesetzt sind. Bis dahin werden
Releases unsigniert (aber mit Herkunftsnachweis) veröffentlicht.

1. **Antrag stellen:** <https://signpath.org/apply> – Projekt `sc-playtime`, Repository
   `https://github.com/hofergeorg-tech/sc-playtime`, Lizenz MIT, Verweis auf diese Datei.
   Die Prüfung dauert erfahrungsgemäß einige Tage bis Wochen.
2. **Nach der Freigabe in SignPath** (app.signpath.io):
   - Projekt mit dem Slug **`sc-playtime`** anlegen bzw. übernehmen.
   - Artefakt-Konfiguration: ZIP mit einer PE-Datei `SC-Playtime.exe` (GitHub liefert
     Artefakte als ZIP).
   - Signatur-Richtlinie mit dem Slug **`release-signing`**.
   - Unter *Trusted Build Systems* GitHub.com mit dem Projekt verbinden.
   - Einen CI-Benutzer mit API-Token anlegen, der für `release-signing` einreichen darf.
3. **In GitHub** (Repository → Settings → Secrets and variables → Actions):
   - Secret **`SIGNPATH_API_TOKEN`** = API-Token des CI-Benutzers
   - Variable **`SIGNPATH_ORGANIZATION_ID`** = Organisations-ID aus SignPath
4. Oben den *Status*-Abschnitt auf den Hinweis „Free code signing provided by …“
   umstellen (verlangt SignPath) und ein neues Release taggen.

Ab dann gilt für jedes Release: Tag pushen → GitHub baut → SignPath signiert (verlangt
die Richtlinie eine Freigabe, bestätigst du sie in der SignPath-Oberfläche; der Workflow
wartet so lange) → Release mit signierter EXE.
