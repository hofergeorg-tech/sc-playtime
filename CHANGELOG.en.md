# Changelog

🇩🇪 [Deutsche Version](CHANGELOG.md)

All notable changes to SC Playtime. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.4.0] – 2026-10-04

### Added
- **Scroll back in the chart:** for DAY, WEEK and MONTH the arrows ‹ › at the top right
  of the chart page into the past, the mouse wheel step by step – back to your first
  session.
- **Analysis** (Menu → Analysis …): heatmap "When do you play?" by weekday and hour, plus
  **playtime per patch**. The Star Citizen version (e.g. 4.3.1) is now read from the
  installation folder and stored with every session.
- **Edit sessions** (Menu → Edit sessions …): correct start and end or delete sessions,
  e.g. after standby with the game left open.
- **AFK detection** (Menu → AFK detection): optionally pause after 5–30 minutes without
  input; the session ends at the last key press and a new one starts with the next
  input. The overlay then shows "AFK".
- **Global hotkeys** (Windows): Ctrl+Shift+F9 shows/hides the overlay, Ctrl+Shift+F11
  toggles "Click-through" – even in game. Change them under Menu → Hotkeys ….
- **Export** of all sessions as CSV (for Excel) or JSON (Menu → Data).
- **Automatic backup:** a copy of the database once a day in `backups`, the last 7 are
  kept; plus "Back up now" in the menu.
- **New languages:** Français, Español, Italiano, Polski and 简体中文 (help and changelog
  in English there).
- **About SC Playtime** in the menu with version, links and a donate button (PayPal).

### Fixed
- The context menu (and the color picker or message boxes) often disappeared behind the
  overlay or behind the game. Menus and dialogs now always stay on top, and the overlay
  no longer pushes itself in front while one is open.

## [1.3.2] – 2026-09-29

### Fixed
- **Chart with channel filter:** with e.g. PTU selected the chart looked the same as
  with ALL, because it always scaled to its own largest bar – 6 minutes of PTU filled
  the height just like 11 hours in total. Now the scale stays that of ALL, the total is
  shown in grey behind, and the selected channel is drawn in its color in front.
  Hovering shows "PTU 6m / 11h 31m".

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
