# Changelog

🇩🇪 [Deutsche Version](CHANGELOG.md)

All notable changes to SC Playtime. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.3.1] – 2026-09-29

### Added
- **Build provenance:** every release file can be verified via GitHub attestation
  (`gh attestation verify …`). Windows code signing via SignPath Foundation has been
  requested and is prepared in the build.
- License: MIT.
- Help: section about the SmartScreen warning.

## [1.3.0] – 2026-09-29

### Added
- **English language:** Menu → Language with flags (🇩🇪 Deutsch, 🇬🇧 English) or
  "Automatic" based on the system language. Overlay, menu, messages, help and changelog
  are fully translated; more languages can be added easily.
- **Linux support:** process detection via `/proc` (including Star Citizen under
  Wine/Proton/Lutris with channel), autostart via `~/.config/autostart`, data in
  `~/.local/share/SC-Playtime`, automatic start via XWayland. Ready-to-run program
  `SC-Playtime-linux-x86_64` in the release, self-update on Linux as well.
- Automatic builds and tests for Windows and Linux via GitHub Actions.

### Fixed
- Message boxes (e.g. "No update") showed dark text on a dark background and looked
  empty.

## [1.2.0] – 2026-09-29

### Added
- **Update function:** checks GitHub for a new version at start and every 12 hours. If
  there is one, a notification appears at the tray icon and "Install update" at the top
  of the menu. The EXE downloads the new version, replaces itself and restarts – the
  running session is saved first.
- Menu: **Check for updates** and **Check for updates automatically** (can be turned off).
- Menu: **Help** and **What's new?** open help and changelog right in the program, also
  offline.
- After an update, "What's new?" is shown once automatically.
- Version number in the menu title and in the windows.

## [1.1.0] – 2026-09-29

### Added
- **Adjustable colors** (Menu → Colors):
  - *Statistic tiles (in game)*: presets Green, Cyan, Amber or "No highlight", plus a
    free choice of background and text color.
  - *Active channel*: presets for the selected channel chip plus a free color choice.
- Statistic tiles are highlighted while the game is running (default: green with dark
  text). When offline they stay dark in HUD style.
- Help (`HILFE.md`) describing all features.

### Fixed
- While the game was running, tiles and channel chips were accidentally filled light
  green, making the white text on them hard to read. The cause was the fill color of the
  status dot, which stayed active afterwards.

## [1.0.0] – 2026-09-28

First release.

### Added
- Frameless overlay in Star Citizen HUD style, always on top.
- Automatic detection of `StarCitizen.exe` (process list, every 2 s, read-only).
- Channel detection from the installation folder: LIVE, PTU, EPTU, HOTFIX, TECH-PREVIEW;
  statistics per channel or combined.
- Multiple games: add and remove any EXE.
- Compact view: session clock, today, week.
- Expanded statistics: tiles (today, week, month, year, total, streak), bar chart
  day / week / month / year / total with hover values, sessions, average and longest
  session.
- Background and overall transparency adjustable separately.
- Lock position, click-through, only show while a game is running.
- Tray icon, single instance, autostart with Windows (no admin).
- Storage in SQLite under `%APPDATA%\SC-Playtime\`; session end saved every 30 s.
- Single EXE build via PyInstaller (`build.py`).
