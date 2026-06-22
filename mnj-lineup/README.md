# MNJ 2026 — Inside Dancefloor Lineup

A static web page that displays the inside-dancefloor DJ lineup for the MNJ 2026
festival, shown on a **CRT TV** driven by a **Raspberry Pi**.

> **How it actually runs:** the Pi is a 2012 Pi 1 (ARMv6, no NEON, 512 MB) that
> can't run Chromium. So instead of a browser, the page is pre-rendered to PNG
> **frames** and shown straight on the console framebuffer with `fbi` — no X, no
> browser, near-zero CPU. The launcher is [`tools/kiosk.sh`](tools/kiosk.sh).
> The web page (`index.html`) is still the source of truth for the design and is
> handy for local preview, but it is **not** what runs at the festival.

The visual style mirrors the ticket site [minijob.lat](https://minijob.lat):
green background, the *Scribble Wire* hand-drawn font, purple monsters, and DJ
names blinking in cycling blue / red / yellow / light-blue.

## End goal

- Pi powers on → boots to a text console on tty1 → `kiosk.sh` shows the correct
  day's frames fullscreen via `fbi`. No keyboard, no mouse, no desktop.
- The festival runs **two nights**:
  - **Day One** — Friday 26 June 2026 (into Saturday morning)
  - **Day Two** — Saturday 27 June 2026 (into Sunday morning)
- The day is picked **by calendar date** with an 8-hour backshift, so a party
  running past midnight still counts as the night it started on:
  - Fri Jun 26 + Sat Jun 27 morning → **Day One**
  - Sat Jun 27 from 08:00 + Sun Jun 28 → **Day Two**
- `pick_day()` only runs **at startup**, so a Pi left running won't auto-flip.
  Plan: power-cycle the TV during the Saturday daytime break to re-pick Day Two,
  or force it manually (see **Manual recovery** below).

## Lineup

**Day One**
```
22:00 - 00:00   Emanuelle
00:00 - 03:00   João Comazzi
03:00 - 06:00   Oph
```

**Day Two**
```
22:00 - 00:00   Elkï
00:00 - 03:00   Panamoil
03:00 - 06:00   Djo
06:00 - 09:00   Chami
10:00 - 13:00   Minijob
```

Lineup data lives in **two** places and must be kept in sync:
- [`js/main.js`](js/main.js) (`LINEUPS`) — the web page.
- [`tools/gen_frames.py`](tools/gen_frames.py) (`LINEUPS`) — the rendered frames
  (this is what the kiosk actually shows). After editing, **re-render the frames**
  (see *Regenerating the frames*).

## Regenerating the frames (on the Mac)

The frames are committed to the repo, so the Pi just `git pull`s them — no
rendering happens on the Pi. Render both modes after any text/layout change:

```bash
cd mnj-lineup/tools
./.venv/bin/python gen_frames.py --mode hdmi        # 1280x720 -> ../kiosk_frames/
./.venv/bin/python gen_frames.py --mode composite   # 720x576 PAL -> ../kiosk_frames_pal/
```

- `hdmi` → `kiosk_frames/day1|day2/frame00-05.png` (for an HDMI display / testing)
- `composite` → `kiosk_frames_pal/day1|day2/...` (overscan-safe for the CRT)

Then commit + push, and on the Pi `git pull` (while still online — the festival
is offline).

## Project structure

```
mnj-lineup/
├── index.html
├── css/style.css            # web preview layout, font, colors, blink
├── js/main.js               # lineup data + day-picking logic (web)
├── assets/
│   ├── fonts/ScribbleWire.ttf
│   ├── monster1.svg         # bottom-left monster
│   └── monster2.svg         # top-right star monster
├── kiosk_frames/            # rendered HDMI frames (day1/, day2/)
├── kiosk_frames_pal/        # rendered PAL composite frames (day1/, day2/)
├── tools/
│   ├── gen_frames.py        # renders the frames (run via .venv)
│   ├── kiosk.sh             # the kiosk launcher (fbi + flicker)
│   ├── flicker.py           # injects 'j' to advance fbi (fake neon blink)
│   └── bash_profile.kiosk   # installed as ~/.bash_profile on the Pi
└── scribble_wire/           # original font download + license
```

## Local preview (web page)

```bash
cd mnj-lineup
python3 -m http.server 8000
# open http://localhost:8000  (press 2 to preview Day Two, 1 for Day One, 0 = auto)
```

---

## Raspberry Pi kiosk

The Pi boots to a text console, autologins on **tty1**, and
[`tools/bash_profile.kiosk`](tools/bash_profile.kiosk) (installed as
`~/.bash_profile`) `exec`s `kiosk.sh`. That script:

1. picks the day (`pick_day()` — date-based, overridable),
2. runs `fbi` once on `/dev/fb0` to show `$MNJ_FRAMES/day$DAY/frame*.png`
   (fbi loops the frames by default — **don't** wrap it in a relaunch loop, that
   causes the black-flash flicker),
3. `exec`s `flicker.py`, which injects the `j` (next image) key into the console
   via the TIOCSTI ioctl every ~0.2 s to drive the fast neon blink.

### kiosk.sh knobs (environment variables)

`kiosk.sh` is configured entirely by env vars, with these defaults:

| Variable       | Default                                          | What it does                                  |
|----------------|--------------------------------------------------|-----------------------------------------------|
| `MNJ_FRAMES`   | `/home/mos/kiosk_frames`                         | Which frame set to show (HDMI vs PAL dir).    |
| `MNJ_TOOLS`    | `/home/mos/static-websites/mnj-lineup/tools`     | Where `flicker.py` lives.                     |
| `MNJ_TTY`      | `/dev/tty1`                                       | Console fbi/flicker drive.                    |
| `MNJ_FLICKER_S`| `0.2`                                             | Seconds between frame advances.               |
| `MNJ_DAY`      | *(unset)*                                         | Force `1` or `2`, bypassing the date logic.   |

The first positional arg to `kiosk.sh` (`1` or `2`) also forces the day and wins
over everything. Precedence: **arg `$1` > `MNJ_DAY` > date**.

> **Note on PAL vs HDMI:** `kiosk.sh` doesn't know about modes — it just shows
> whatever directory `MNJ_FRAMES` points at. The Pi default
> (`/home/mos/kiosk_frames`) is a symlink to the repo's `kiosk_frames/`. To run
> the PAL set, point `MNJ_FRAMES` at `.../mnj-lineup/kiosk_frames_pal` (see below).

---

## Manual recovery at the venue

If the kiosk comes up on the **wrong day** (clock/NTP wrong) or you need to swap
the **frame set**, you don't need the laptop — plug a USB keyboard into the Pi.
On tty1 the kiosk is running; switch to a free console with **Ctrl+Alt+F2**, log
in (user `mos`, password auth), then use one of the recipes below. Switch back to
the live screen with **Ctrl+Alt+F1**.

Path reminders on the Pi:
- frames repo: `/home/mos/static-websites/mnj-lineup/`
- HDMI frames: `.../mnj-lineup/kiosk_frames`  (and the `~/kiosk_frames` symlink)
- PAL frames:  `.../mnj-lineup/kiosk_frames_pal`

### 1. Force a specific day (quickest fix)

Stop the running kiosk and relaunch it pinned to a day. Run **on tty1** (so fbi
draws to the screen you're looking at):

```bash
# Kill whatever's driving the screen
sudo pkill -f flicker.py ; sudo pkill fbi

# Relaunch pinned to Day One (use 2 for Day Two). $1 wins over the date.
sh /home/mos/static-websites/mnj-lineup/tools/kiosk.sh 1
```

Equivalently via the env var:

```bash
sudo pkill -f flicker.py ; sudo pkill fbi
MNJ_DAY=2 sh /home/mos/static-websites/mnj-lineup/tools/kiosk.sh
```

> If you ran the relaunch from a *different* console (e.g. tty2), pass the tty so
> fbi targets tty1: `MNJ_TTY=/dev/tty1 MNJ_DAY=2 sh .../kiosk.sh` — then switch
> to it with Ctrl+Alt+F1.

To make the forced day **stick across reboots**, set it in the launcher:

```bash
# Edit ~/.bash_profile and change the kiosk line to force a day, e.g.:
#   exec env MNJ_DAY=2 /home/mos/static-websites/mnj-lineup/tools/kiosk.sh
nano ~/.bash_profile
```

Remember to undo that after the festival, or it'll be stuck on that day.

### 2. Force the frame set (HDMI ↔ PAL)

Point `MNJ_FRAMES` at the directory you want:

```bash
sudo pkill -f flicker.py ; sudo pkill fbi

# Show the PAL composite set (good for the CRT):
MNJ_FRAMES=/home/mos/static-websites/mnj-lineup/kiosk_frames_pal \
  sh /home/mos/static-websites/mnj-lineup/tools/kiosk.sh

# ...or combine with a forced day:
MNJ_FRAMES=/home/mos/static-websites/mnj-lineup/kiosk_frames_pal MNJ_DAY=2 \
  sh /home/mos/static-websites/mnj-lineup/tools/kiosk.sh
```

To make PAL the default, repoint the symlink the launcher uses:

```bash
ln -sfn /home/mos/static-websites/mnj-lineup/kiosk_frames_pal /home/mos/kiosk_frames
```

(Point it back at `.../kiosk_frames` to return to the HDMI set.)

### 3. Show a single image with no kiosk logic (last resort)

If `kiosk.sh` itself is misbehaving, you can drive `fbi` directly — e.g. to put
Day Two on screen immediately:

```bash
sudo pkill -f flicker.py ; sudo pkill fbi
fbi -d /dev/fb0 -T 1 -a --noverbose \
  /home/mos/static-websites/mnj-lineup/kiosk_frames/day2/frame*.png
```

(Swap `kiosk_frames` → `kiosk_frames_pal` for the CRT set, `day2` → `day1` for
the other night. This loops the frames but without the fast `flicker.py` blink.)

### 4. Fix the clock so auto-pick works

The board has no RTC battery, so an offline cold boot can have the wrong date.
If you can get it online briefly (phone hotspot), let it NTP-sync, then a normal
reboot will auto-pick correctly:

```bash
date                                  # check what the Pi thinks it is
sudo systemctl restart systemd-timesyncd   # re-sync if online
sudo reboot
```

If you can't get online, just force the day with recipe **1** — that's the
reliable path at the venue.

### Festival-day checklist

- ✅ `git pull` the latest frames onto the Pi **while still online** (festival is
  offline; the Pi can't render).
- ✅ Pi clock is correct (`date`) — the day auto-picks from it. TZ is
  Europe/Berlin; NTP-sync once on arrival via a hotspot.
- ✅ Boot once and verify the right night shows. If the clock can't be trusted,
  plug in a keyboard and use **Manual recovery → Force a specific day**.
- ✅ Saturday daytime: power-cycle the TV during the break so it re-picks Day Two
  (or force `MNJ_DAY=2`).
