# MNJ 2026 — Inside Dancefloor Lineup

A static web page that displays the inside-dancefloor DJ lineup for the MNJ 2026
festival, shown on a **CRT TV at 1280×720 (16:9)** driven by a **Raspberry Pi**
running Chromium in fullscreen kiosk mode at boot.

The visual style mirrors the ticket site [minijob.lat](https://minijob.lat):
green background, the *Scribble Wire* hand-drawn font, purple monsters, and DJ
names blinking in cycling blue / red / yellow / light-blue.

## End goal

- Pi powers on → boots straight into fullscreen Chromium → shows the correct
  day's lineup. No keyboard, no mouse, no desktop.
- The festival runs **two nights**:
  - **Day One** — Friday 26 June 2026 (into Saturday morning)
  - **Day Two** — Saturday 27 June 2026 (into Sunday morning)
- The page picks the day **by calendar date**, with an 8-hour backshift so that
  when the clock rolls past midnight the party still counts as the night it
  started on:
  - Fri Jun 26 + Sat Jun 27 until ~14:00 → **Day One**
  - Sat Jun 27 afternoon + Sun Jun 28 until ~14:00 → **Day Two**

## Lineup

**Day One**
```
22:00 - 23:00   Emanuelle
23:00 - 00:00   Emanuelle
00:00 - 03:00   João Comazzi
03:00 - 06:00   Oph
```

**Day Two**
```
22:00 - 00:00   Elkï
00:00 - 03:00   Panamoil
03:00 - 06:00   Jo
06:00 - 09:00   Chami
10:00 - 13:00   Minijob
```

Lineup data lives in [`js/main.js`](js/main.js) (`LINEUPS`). Edit there to change
times or names.

## Switching the day manually

The Pi should pick the day automatically, but if its clock is wrong you can
override:

- **Keyboard:** press `1` (Day One), `2` (Day Two), or `0` (back to auto).
  The choice is saved in `localStorage` and survives reloads/reboots.
- **URL:** `index.html?day=1` or `index.html?day=2`.

## Project structure

```
mnj-lineup/
├── index.html
├── css/style.css          # 1280×720 layout, font, colors, blink
├── js/main.js             # lineup data + day-picking logic
├── assets/
│   ├── fonts/ScribbleWire.ttf
│   ├── monster1.svg       # bottom-left monster
│   └── monster2.svg       # top-right star monster
└── scribble_wire/         # original font download + license
```

## Local preview

```bash
cd mnj-lineup
python3 -m http.server 8000
# open http://localhost:8000  (press 2 to preview Day Two)
```

---

## Raspberry Pi kiosk setup

Target: Raspberry Pi OS (with desktop), auto-login enabled, Chromium launched
at boot via a **systemd service**. Files live in a local clone and load over
`file://` (no network needed at the festival).

### 1. Get the files onto the Pi

```bash
git clone <this-repo-url> /home/pi/mnj-lineup
```

The lineup page is then at:
`file:///home/pi/mnj-lineup/index.html`

### 2. Install Chromium and unclutter

```bash
sudo apt update
sudo apt install -y chromium-browser unclutter
```

(`unclutter` hides the mouse pointer; the page also sets `cursor: none`.)

### 3. Enable desktop auto-login

```bash
sudo raspi-config
# System Options → Boot / Auto Login → Desktop Autologin
```

This ensures a graphical session (X / the desktop) is running for Chromium to
draw into.

### 4. Create the kiosk launch script

`/home/pi/mnj-lineup/kiosk.sh`:

```bash
#!/usr/bin/env bash
set -e

export DISPLAY=:0

# Stop the screen from blanking / dimming
xset s off
xset -dpms
xset s noblank

# Hide the cursor after 0.1s of inactivity
unclutter -idle 0.1 &

# Clear Chromium's "didn't shut down cleanly" restore prompt
PROFILE="$HOME/.config/chromium/Default/Preferences"
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' "$PROFILE" 2>/dev/null || true
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/'   "$PROFILE" 2>/dev/null || true

exec chromium-browser \
  --kiosk \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-restore-session-state \
  --check-for-update-interval=31536000 \
  --window-size=1280,720 \
  --window-position=0,0 \
  --autoplay-policy=no-user-gesture-required \
  "file:///home/pi/mnj-lineup/index.html"
```

Make it executable:

```bash
chmod +x /home/pi/mnj-lineup/kiosk.sh
```

> On newer Raspberry Pi OS the binary may be `chromium` instead of
> `chromium-browser` — adjust the script if so (`which chromium`).

### 5. Create the systemd service

`/etc/systemd/system/mnj-kiosk.service`:

```ini
[Unit]
Description=MNJ 2026 Lineup Kiosk (Chromium fullscreen)
After=graphical.target
Wants=graphical.target

[Service]
User=pi
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/home/pi/mnj-lineup/kiosk.sh
Restart=always
RestartSec=5

[Install]
WantedBy=graphical.target
```

### 6. Enable and start

```bash
sudo systemctl daemon-reload
sudo systemctl enable mnj-kiosk.service
sudo systemctl start mnj-kiosk.service
```

Reboot to confirm it comes up on its own:

```bash
sudo reboot
```

### Useful commands

```bash
# Check status / logs
systemctl status mnj-kiosk.service
journalctl -u mnj-kiosk.service -f

# Restart after editing files or the script
sudo systemctl restart mnj-kiosk.service

# Disable kiosk (back to normal desktop)
sudo systemctl disable --now mnj-kiosk.service
```

### Festival-day checklist

- ✅ Pi clock is correct (`date`) — the day auto-picks from it.
  Set timezone via `sudo raspi-config` → Localisation → Timezone.
- ✅ CRT set to a 1280×720 / 16:9 mode (check `/boot/config.txt` HDMI settings
  if the picture is cropped or off-center).
- ✅ Boot once before the event and verify the right night shows; if the clock
  can't be trusted, plug in a keyboard and press `1` / `2`.
- ✅ Screen blanking disabled (handled by the `xset` lines in `kiosk.sh`).
