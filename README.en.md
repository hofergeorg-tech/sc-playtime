# SC Playtime

🇩🇪 [Deutsch](README.md)

A mini overlay in Star Citizen HUD style that tracks your playtime – for **Windows** and
**Linux**, in **English** and **German**.

📥 **[Download](https://github.com/hofergeorg-tech/sc-playtime/releases/latest)** ·
📖 **[Help – all features explained](HELP.md)** · 📝 **[Changelog](CHANGELOG.en.md)**

- detects `StarCitizen.exe` automatically (every 2 s, only reads the process list) – on
  Linux also via Wine/Proton/Lutris
- **Channel from the installation folder**: `…\StarCitizen\LIVE\Bin64\StarCitizen.exe` → LIVE,
  likewise PTU, EPTU, HOTFIX, TECH-PREVIEW — per channel or combined ("ALL")
- **Multiple games**: add any program via right-click → Game → Add game …
- Display: running session (large clock), today / week; expanded: month, year, total,
  streak (consecutive days), sessions, average and longest session, bar chart
  day (14) / week (12) / month (12) / year (5) with hover values
- Transparency: background and overall opacity via separate sliders
- Colors: statistic tiles are highlighted in game (default green with dark text); tiles
  and the active channel chip adjustable via presets or free color choice
- Language: English / Deutsch with flags in the menu, or automatic based on the system
- Autostart (Windows: HKCU\…\Run, Linux: `~/.config/autostart`), tray icon, single instance
- Update check via GitHub Releases with self-update; help and "What's new?" right in the
  menu

## Run from source

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

Star Citizen must run in **borderless window** mode, otherwise no overlay can be drawn
on top (applies to all overlays). Linux specifics (Wayland, GNOME tray): see
[Help → Linux](HELP.md#linux).

## Data

Windows `%APPDATA%\SC-Playtime\`, Linux `~/.local/share/SC-Playtime/`

- `playtime.db` — SQLite, table `sessions(game, channel, start, end)`
- `settings.json` — position, transparency, colors, language, game list …

## Build

```powershell
.venv\Scripts\pip install pyinstaller
.venv\Scripts\python.exe build.py      # → dist\SC-Playtime.exe (Linux: dist/SC-Playtime)
```

## Publishing a release

1. Bump the version in `sc_playtime/__init__.py`, extend `CHANGELOG.md` and `CHANGELOG.en.md`.
2. Commit, tag and push: `git tag v1.4.0 && git push --tags`
3. GitHub Actions ([ci.yml](.github/workflows/ci.yml)) runs the tests, builds the
   Windows and Linux programs and creates the release with both files. Installed
   overlays then find the update by themselves.

## Translating

Texts live in [sc_playtime/i18n.py](sc_playtime/i18n.py). New language: add a table,
put the flag at `assets/flags/<code>.svg`, optionally translate help/changelog and
register them in `DOCS`.

## Tests

```powershell
python -m unittest discover -s tests
```
