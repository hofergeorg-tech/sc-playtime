# SC Playtime – Help

🇩🇪 [Deutsche Version](HILFE.md)

SC Playtime is a small overlay that tracks how long you play Star Citizen (or other
games). It sits as a slim panel on top of the game and shows the running session and
your statistics. It runs on **Windows** and **Linux**.

- [Installation and start](#installation-and-start)
- [The overlay](#the-overlay)
- [Mouse controls](#mouse-controls)
- [The menu](#the-menu)
- [Colors](#colors)
- [Language](#language)
- [Multiple games](#multiple-games)
- [Channels (LIVE, PTU, …)](#channels-live-ptu-)
- [How time is counted](#how-time-is-counted)
- [Updates](#updates)
- [Linux](#linux)
- [Your data](#your-data)
- [FAQ](#faq)

---

## Installation and start

**Windows:** download `SC-Playtime.exe` from the
[release page](https://github.com/hofergeorg-tech/sc-playtime/releases/latest), put it in
its own folder (e.g. `Documents\SC-Playtime`) and run it. No installation needed; the
tray icon (a clock in a frame) appears at the bottom right of the taskbar.

**Linux:** see [Linux](#linux).

**From source (Windows):**

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pythonw.exe run.pyw
```

Only one instance runs at a time. A second start (e.g. autostart plus a manual start)
exits immediately so nothing is counted twice.

> **Important:** Star Citizen must run in **"Borderless window"** mode. In exclusive
> fullscreen no overlay can be drawn on top – this applies to all overlays.

## The overlay

### Compact view

| Element | Meaning |
| --- | --- |
| Dot at the top left | pulses green while the game is running; grey when offline |
| Game name | the displayed game, next to it the channel (e.g. **LIVE**) |
| **IN GAME** / **OFFLINE** | status at the top right |
| Large clock | length of the running session; when offline, the length of the last one |
| TODAY / WEEK | played today and since Monday of this week |

### Expanded statistics

Clicking the header of the overlay expands or collapses the statistics.

- **Channel filter** (ALL, LIVE, PTU, …): shows the statistics for one channel or all of
  them together. Appears once sessions with a channel have been recorded.
- **Tiles:**

  | Tile | Meaning |
  | --- | --- |
  | TODAY | playtime since midnight |
  | WEEK | since Monday 0:00 |
  | MONTH | since the 1st of the month |
  | YEAR | since January 1st |
  | TOTAL | everything ever recorded |
  | STREAK | consecutive days with at least 1 minute of playtime. Not having played yet today does not break the streak. |

- **Chart** with the tabs:

  | Tab | shows |
  | --- | --- |
  | DAY | the last 14 days |
  | WEEK | the last 12 calendar weeks |
  | MONTH | the last 12 months |
  | YEAR | the last 5 years |
  | TOTAL | every year since your first session |

  The current period is highlighted in green. Hover over a bar to see the exact period
  and playtime at the bottom.

  With a channel filter active (e.g. PTU), the colored bars show only that channel.
  Behind them, the total of all channels is shown in grey and the scale stays the same
  as for "ALL" – so you can see at a glance which share belongs to the channel. Hovering
  shows e.g. "PTU 6m / 11h 31m" at the bottom.
- **Footer:** number of sessions, average and longest session (sessions under 1 minute
  are not counted here).

## Mouse controls

| Action | Effect |
| --- | --- |
| Click the header | expand/collapse statistics |
| Drag with the left mouse button | move the overlay (unless "Lock position" is on) |
| Click a channel chip | set the channel filter |
| Click a tab | change the chart period |
| Hover over a bar | exact values in the footer |
| Right-click the overlay | menu |
| Left-click the tray icon | show/hide the overlay |
| Right-click the tray icon | menu (also when the overlay is hidden) |

Position, expanded state, selected tab and filter are saved and restored on the next
start.

## The menu

| Entry | Function |
| --- | --- |
| Show/Hide overlay | tray menu only |
| Show statistics | same as clicking the header |
| Game | choose the displayed game, add or remove games |
| BACKGROUND (slider) | opacity of the dark background only; text stays fully visible |
| OVERALL OPACITY (slider) | opacity of the whole overlay (20–100 %) |
| Colors | see [Colors](#colors) |
| Language | see [Language](#language) |
| Lock position | the overlay can no longer be moved |
| Click-through | mouse clicks pass through the overlay into the game. Can only be turned off via the **tray icon**. |
| Only show while a game is running | the overlay hides itself automatically when offline |
| Start with Windows / Start on login | autostart on login (no admin rights needed) |
| Help … | this help |
| What's new? … | changelog with all changes per version |
| Check for updates | check GitHub right away, see [Updates](#updates) |
| Check for updates automatically | check at start and every 12 hours (default: on) |
| ⬆ Install update … | appears at the top when a new version is available |
| Open data folder | opens the folder with database and settings |
| Quit | close the overlay; the running session is saved first |

## Colors

**Menu → Colors** has two sections. Each has presets plus "Choose background color …"
and "Choose text color …" for your own colors.

**Statistic tiles (in game)** – when offline the tiles are always dark in HUD style. As
soon as the game runs, they are highlighted:

- Green / Dark (default)
- Cyan / Dark
- Amber / Dark
- No highlight (HUD) – tiles stay dark in game too

**Active channel** – the selected channel chip (in the header and the filter):

- Automatic – the channel's color (LIVE green, PTU yellow, …) with dark text
- Dark green / White, Black / Green, Dark blue / White, White / Black

Tip: for good readability combine light backgrounds with dark text and vice versa.

## Language

**Menu → Language** (with flag) offers:

- **Automatic (system)** – default; German if your operating system is set to German,
  English otherwise
- 🇩🇪 **Deutsch**
- 🇬🇧 **English**

The change applies immediately to the overlay, menu, messages, help and "What's new?".

## Multiple games

`StarCitizen.exe` is tracked by default. To add more games:

1. Right-click → **Game → Add game …**
2. Choose the game's program (Windows: the `.exe`; Linux: see below).
3. Enter a display name.

Games are recognised by their program name. While a game runs, the overlay shows it
automatically; if several run, the one selected in the menu. **Remove game** stops
tracking a game – its existing sessions are kept.

## Channels (LIVE, PTU, …)

The channel is read from the installation folder:

```
…\StarCitizen\LIVE\Bin64\StarCitizen.exe   →  LIVE
…\StarCitizen\PTU\Bin64\StarCitizen.exe    →  PTU
```

Likewise EPTU, HOTFIX and TECH-PREVIEW. Every session remembers its channel, so the
statistics can be shown per channel or combined ("ALL").

## How time is counted

- The process list is read every 2 seconds. It is only **read** – nothing is injected
  into the game.
- If you start the overlay while the game is already running, the session still counts
  from the real start of the game.
- The end of the session is saved every 30 seconds. If the PC crashes, at most those 30
  seconds are lost.
- Sessions across midnight (or week/month boundaries) are split proportionally.

## Updates

The current version is shown at the top of the menu (e.g. "SC PLAYTIME 1.3.0").

- **Automatic:** with "Check for updates automatically" on, SC Playtime checks GitHub
  for a new version shortly after start and then every 12 hours. If there is one, a
  notification appears at the tray icon and the entry **"⬆ Install update …"** appears at
  the top of the menu.
- **Manual:** Menu → "Check for updates".
- **Install:** after confirming, the new version is downloaded. The overlay saves the
  running session, exits, replaces the program file and restarts. Afterwards "What's
  new?" is shown once. Settings and playtimes are kept.
- When SC Playtime runs from source instead of as a built program, "Install" opens the
  release page in your browser instead.

All versions are also available at
<https://github.com/hofergeorg-tech/sc-playtime/releases>.

## Linux

**Built program:** download `SC-Playtime-linux-x86_64` from the
[release page](https://github.com/hofergeorg-tech/sc-playtime/releases/latest), put it
e.g. in `~/Applications/`, make it executable and run it:

```bash
chmod +x SC-Playtime-linux-x86_64
./SC-Playtime-linux-x86_64
```

**From source:**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.pyw
```

Notes:

- **Star Citizen under Wine/Proton/Lutris** is detected just like on Windows – including
  the channel (LIVE, PTU, …), because the game's Windows path is read as well.
- **Native Linux games:** add them via "Add game …" with the game's program (set the
  file filter to "All files"). They are recognised by their program name.
- **Wayland:** under Wayland, windows may neither choose their position nor stay on top.
  SC Playtime therefore starts via **XWayland** automatically, which almost every
  desktop provides. Set `QT_QPA_PLATFORM` yourself to override this.
- **Tray icon on GNOME:** GNOME only shows tray icons with the extension "AppIndicator
  and KStatusNotifierItem Support". KDE, XFCE, Cinnamon etc. need nothing.
- **Autostart** is called "Start on login" in the menu and creates
  `~/.config/autostart/sc-playtime.desktop`.
- **Data** is stored in `~/.local/share/SC-Playtime/`.

## Your data

Everything is stored locally (Menu → "Open data folder"):

- Windows: `%APPDATA%\SC-Playtime\`
- Linux: `~/.local/share/SC-Playtime/`

| File | Content |
| --- | --- |
| `playtime.db` | SQLite database with all sessions (game, channel, start, end) |
| `settings.json` | position, transparency, colors, language, game list, … |

Your playtimes and settings never leave your PC. The only internet connection is the
update check: it only fetches the public version info from GitHub and can be turned off
in the menu. To back up or move your data, just copy the folder. To reset the settings,
delete `settings.json` while the overlay is closed.

## FAQ

**The overlay is not visible in game.**
Set Star Citizen to "Borderless window". Check whether the overlay was hidden via the
tray icon.

**I can't click the overlay anymore.**
"Click-through" is on. Right-click the tray icon and untick it.

**The overlay has disappeared.**
Left-clicking the tray icon shows it again. With "Only show while a game is running"
enabled it does not appear while offline.

**Autostart no longer works.**
The entry points to the location of the program or of `run.pyw`. After moving the
folder, turn autostart off and on again in the menu.

**The update fails.**
Check your internet connection and try again with "Check for updates". If the program
is in a protected folder (e.g. `C:\Program Files` or `/usr/bin`), it cannot replace
itself – download the new version from the release page or move the program to its own
folder.

**Windows says "Windows protected your PC".**
The EXE is not digitally signed yet (requested, see [CODE_SIGNING.md](CODE_SIGNING.md)),
so SmartScreen warns about new downloads. Click "More info" → "Run anyway". To verify
that the file really was built from this repository:
`gh attestation verify SC-Playtime.exe --repo hofergeorg-tech/sc-playtime`

**Does this interfere with anti-cheat?**
SC Playtime only reads the process list and the game's start time using regular
operating system functions, just like the Task Manager. It does not access the game.
