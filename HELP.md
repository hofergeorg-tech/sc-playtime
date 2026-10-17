# SC Playtime – Help

🇩🇪 [Deutsch](HILFE.md) · 🇫🇷 [Français](HELP.fr.md) · 🇪🇸 [Español](HELP.es.md) · 🇮🇹 [Italiano](HELP.it.md) · 🇵🇱 [Polski](HELP.pl.md) · 🇨🇳 [简体中文](HELP.zh.md)

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
- [Analysis (heatmap, day timeline, patches)](#analysis-heatmap-day-timeline-patches)
- [Editing sessions](#editing-sessions)
- [AFK detection](#afk-detection)
- [Anti-AFK](#anti-afk)
- [Hotkeys](#hotkeys)
- [Export and backup](#export-and-backup)
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
| Dot at the top left | pulses green while the game is running; yellow when AFK; grey when offline |
| Game name | the displayed game, next to it the channel (e.g. **LIVE**) |
| **IN GAME** / **AFK** / **OFFLINE** | status at the top right (AFK see [AFK detection](#afk-detection)) |
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
  | TOTAL | everything ever recorded; at the top right the date of the first recording (since when counting started) |
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

  **Scrolling back** (DAY, WEEK, MONTH): the arrows ‹ › at the top right of the chart
  jump half a chart into the past or back towards today. Use the **mouse wheel** over
  the chart for single steps (up = older). You can't scroll back further than your first
  session. Switching the tab or filter jumps back to today.

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
| Click ‹ / › on the chart | scroll back / forward |
| Mouse wheel over the chart | one period back (up) or forward (down) |
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
| Analysis … | heatmap, day timeline and playtime per patch, see [Analysis](#analysis-heatmap-day-timeline-patches) |
| Edit sessions … | correct or delete sessions, see [Editing sessions](#editing-sessions) |
| BACKGROUND (slider) | opacity of the dark background only; text stays fully visible |
| OVERALL OPACITY (slider) | opacity of the whole overlay (20–100 %) |
| Colors | see [Colors](#colors) |
| Language | see [Language](#language) |
| Lock position | the overlay can no longer be moved |
| Click-through | mouse clicks pass through the overlay into the game. Can only be turned off via the **tray icon** or the [hotkey](#hotkeys). |
| Only show while a game is running | the overlay hides itself automatically when offline |
| AFK detection | don't count time without input, see [AFK detection](#afk-detection) |
| Hotkeys … | global keys to show/hide, see [Hotkeys](#hotkeys) |
| Start with Windows / Start on login | autostart on login (no admin rights needed) |
| Help … | this help |
| What's new? … | changelog with all changes per version |
| About SC Playtime … | version, links, license and donate button (PayPal) |
| Check for updates | check GitHub right away, see [Updates](#updates) |
| Check for updates automatically | check at start and every 12 hours (default: on) |
| ⬆ Install update … | appears at the top when a new version is available |
| Data | export as CSV/JSON, backups, sessions from another PC, data folder, see [Export and backup](#export-and-backup) |
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

- **Automatic (system)** – default; the language of your operating system if supported,
  English otherwise
- 🇩🇪 **Deutsch**
- 🇬🇧 **English**
- 🇫🇷 **Français**, 🇪🇸 **Español**, 🇮🇹 **Italiano**, 🇵🇱 **Polski**, 🇨🇳 **简体中文**

The change applies immediately to the overlay, menu, messages, help and "What's new?" –
help and changelog are available in all seven languages.

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

## Analysis (heatmap, day timeline, patches)

**Menu → Analysis …** opens a window for the displayed game and the selected channel
filter:

- **When do you play?** – a heatmap with the weekdays as rows and the 24 hours as
  columns. The brighter a cell, the more you played at that time. Hover over a cell for
  the exact playtime; below it shows your most played weekday and hour.
- **Day timeline** – one day as a timeline from 0 to 24 h: every session is a bar in the
  color of its channel, gaps are breaks or AFK time. A **red mark** at the end of a
  session means a crash, a **yellow** one a server disconnect. Use ‹ › to move between
  the days you played; hover over a bar for time, length, channel, patch and how the
  session ended.
- **Playtime per patch** – playtime, share, number of sessions, **crashes**, **server
  disconnects** and period for each Star Citizen version (e.g. 4.3.1). For crashes it also
  shows how often they happened, e.g. "2 · every 6h 30m" – so you can see whether a patch
  is more stable than the previous one. The patch is read from `build_manifest.id` or
  `Game.log` in the installation folder (e.g. `…\StarCitizen\LIVE\`) when a session
  starts. Sessions from before version 1.4 and games without these files are listed as
  "unknown".

### Crashes and server disconnects

When Star Citizen closes, SC Playtime reads the end of `Game.log` (read only):

| In the log | Meaning |
| --- | --- |
| `<SystemQuit>` with "Quit via console command" / "User closed the application" | **quit** – you stopped playing yourself |
| `<SystemQuit>` with another reason, e.g. "Back-end services are unresponsive" | **server disconnect** – connection to the server/backend lost |
| no `<SystemQuit>` line, but a hand-over to the crash collector | **crash** |

Older sessions are classified when SC Playtime starts: Star Citizen keeps the log of every
game start in its `logbackups` folder, and the matching log is found by the time the
session ended. Sessions without a log, games other than Star Citizen and sessions that
ended in an AFK break can't be classified. The installation is found automatically (the
default folder or the folder the game ran from).

## Editing sessions

**Menu → Edit sessions …** lists all sessions of the displayed game, newest first. Use
it to fix mistakes, e.g. when the PC was in standby while the game was open:

- The **Outcome** column shows how the session ended: quit, **crash** (red) or **server
  disconnect** (yellow), see [Crashes and server disconnects](#crashes-and-server-disconnects).
- **Edit …** (or double-click): change start and end.
- **Delete**: remove one or more selected sessions (Ctrl/Shift for multiple selection).
  This cannot be undone – [back up](#export-and-backup) first if in doubt.

The running session (green, "running") is locked until the game is closed.

## AFK detection

**Menu → AFK detection** lets you exclude time without input: **Off** (default) or
pause after **5, 10, 15 or 30 minutes** without keyboard, mouse or controller input.

- Once the time is reached, the session ends at your **last key press** – so the waiting
  time itself doesn't count either. The overlay shows **AFK** with a yellow dot.
- As soon as there is input again and the game is still running, a new session starts
  automatically.
- Any input on the PC counts, not just in the game.
- On Linux this works under X11/XWayland (library `libXss`); without it the detection
  has no effect.

## Anti-AFK

Star Citizen kicks you out after a while without input. **Menu → Anti-AFK** keeps the game
awake (**Windows** only):

- **Anti-AFK active** is the main switch (also **Ctrl+Shift+F12**). While it is on, the chosen
  actions run on their interval – even while you are playing yourself.
- **Press key:** presses the key right of P ([ on US, Ü on German keyboards), every 5 s by
  default. Best not to bind anything to it in the game.
- **Move mouse:** traces a small pattern (right–left, up–down, square, circle or random) and
  ends where it started. **Distance** (1–100 pixels), **speed** and **mouse interval** can be set.
- Input is sent **only while the game is in the foreground** – so you never type into a chat
  or another window by accident.
- Real key scancodes are sent; Star Citizen ignores plain key codes (as sent by “Move Mouse”).
- **Rings in the overlay:** next to the clock one ring each shows the interval of key and
  mouse, and the overlay shows **ANTI-AFK**. Click a ring to turn that action on or off.
- Anti-AFK input does not count as activity: [AFK detection](#afk-detection) still pauses
  when you do nothing yourself.

## Hotkeys

Global hotkeys work everywhere, even while the game is in the foreground (**Windows**
only):

| Default | Effect |
| --- | --- |
| **Ctrl+Shift+F9** | show/hide the overlay |
| **Ctrl+Shift+F11** | turn "Click-through" on/off |
| **Ctrl+Shift+F12** | turn Anti-AFK on/off |

Change them under **Menu → Hotkeys …**: click a field, press the new combination, clear
it with ✕ (= no hotkey). Letters, digits, F1–F24, Home/End/Ins/Del, PgUp/PgDown, arrow
keys, Pause and Space are allowed – except for the F keys always with Ctrl, Shift, Alt
or Win. If a combination is already used by another program, you'll get a notice.

## Export and backup

Under **Menu → Data**:

| Entry | Function |
| --- | --- |
| Export as CSV … | all sessions of all games as a table, e.g. for Excel (columns: game, channel, patch, start, end, duration in seconds and minutes, ending `quit`/`crash`/`server`) |
| Export as JSON … | the same as JSON, times additionally with time zone and as Unix timestamps |
| Back up now | create a copy of the database right away |
| Daily automatic backup (7 days) | create a copy once a day; the last 7 are kept (default: on) |
| Open backup folder | folder `backups` inside the data folder |
| Import sessions from another PC … | add the playtime of a second PC, see below |
| Open data folder | folder with database and settings |

**Restoring a backup:** quit the overlay, replace `playtime.db` in the data folder with
the file you want from `backups` (e.g. copy `playtime-2026-10-04.db` and rename it to
`playtime.db`), start the overlay again.

### Combining two PCs

If you play on several PCs, add the other PC's playtime like this:

1. On the other PC, take the file `playtime.db` from the data folder (or a backup from
   `backups`), e.g. via USB stick or a cloud folder.
2. Here, choose **Menu → Data → Import sessions from another PC …** and pick the file.
3. SC Playtime shows how many sessions are new and how many are already here, and after
   you confirm imports only the new ones. The current data is backed up first.

A session counts as "already here" if it overlaps in time with a session of the same
game here – the same game doesn't run on two PCs at once. That's why you can import the
same file again later without anything being counted twice. Channel, patch and ending
are imported too. Games that don't exist here yet are named: their sessions are saved and
show up as soon as you add the game with the same name.

## How time is counted

- The process list is read every 2 seconds. It is only **read** – nothing is injected
  into the game.
- If you start the overlay while the game is already running, the session still counts
  from the real start of the game.
- The end of the session is saved every 30 seconds. If the PC crashes, at most those 30
  seconds are lost.
- Sessions across midnight (or week/month boundaries) are split proportionally.

## Updates

The current version is shown at the top of the menu (e.g. "SC PLAYTIME 1.5.0").

- **Automatic:** with "Check for updates automatically" on, SC Playtime checks GitHub
  for a new version shortly after start and then every 12 hours. If there is one, a
  notification appears at the tray icon and the entry **"⬆ Install update …"** appears at
  the top of the menu.
- **Manual:** Menu → "Check for updates".
- **Install:** after confirming, the new version is downloaded and compared with the
  checksum GitHub reports for the release – if it doesn't match, nothing is installed.
  The overlay saves the running session, exits, replaces the program file and restarts.
  Afterwards "What's new?" is shown once. Settings and playtimes are kept.
- When SC Playtime runs from source (`run.pyw`) instead of as a built program, "Install"
  opens the release page in your browser instead – there is no program file to replace.
  For one-click updates, use the EXE and turn autostart off and on again in the menu.

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
  the channel (LIVE, PTU, …), because the game's Windows path is read as well. Crashes
  and server disconnects are only detected on Windows.
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
| `playtime.db` | SQLite database with all sessions (game, channel, start, end, patch, ending) |
| `settings.json` | position, transparency, colors, language, game list, Star Citizen folders found, … |
| `backups/` | daily copies of the database, see [Export and backup](#export-and-backup) |

Your playtimes and settings never leave your PC. The only internet connection is the
update check: it only fetches the public version info from GitHub and can be turned off
in the menu. To back up or move your data, just copy the folder. To reset the settings,
delete `settings.json` while the overlay is closed.

## FAQ

**The overlay is not visible in game.**
Set Star Citizen to "Borderless window". Check whether the overlay was hidden via the
tray icon.

**I can't click the overlay anymore.**
"Click-through" is on. Press **Ctrl+Shift+F11**, or right-click the tray icon and untick
it.

**The menu or a window appears behind the game.**
Since version 1.4, menus and dialogs are always shown in front of the overlay and the
game. If a window is still hidden, switch to it with Alt+Tab.

**The playtime is wrong because I left the game open.**
Correct the session under **Menu → Edit sessions …** and turn on
[AFK detection](#afk-detection) for the future.

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
operating system functions, just like the Task Manager, and after the game has closed
the text file `Game.log`. It does not access the game.

**A session has no ending.**
The log showed neither a normal end nor a crash – e.g. when Star Citizen was ended via
the Task Manager, the power went out, the session ended in an AFK break or there is no
log for it anymore. The classification is only used for the statistics and doesn't
change the playtime.
