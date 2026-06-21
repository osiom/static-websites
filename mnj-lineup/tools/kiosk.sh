#!/bin/sh
# MNJ 2026 framebuffer kiosk.
# Picks the day's frame set by date (8h backshift so a party running past
# midnight still counts as the night it started on), shows the frames with fbi
# on the console framebuffer, and drives a fast frame advance via TIOCSTI
# (flicker.py) to fake the neon blink. One fbi process, no relaunch thrash.
#
#   Fri Jun 26 2026 -> day1
#   Sat Jun 27 2026 -> day2
# Override: pass 1 or 2 as $1, or set MNJ_DAY=1|2 in the environment.

FRAMES_DIR="${MNJ_FRAMES:-/home/mos/kiosk_frames}"
TOOLS_DIR="${MNJ_TOOLS:-/home/mos/static-websites/mnj-lineup/tools}"
TTY="${MNJ_TTY:-/dev/tty1}"
FLICKER_S="${MNJ_FLICKER_S:-0.2}"   # seconds between frame advances

pick_day() {
  if [ "$1" = "1" ] || [ "$1" = "2" ]; then echo "$1"; return; fi
  if [ "$MNJ_DAY" = "1" ] || [ "$MNJ_DAY" = "2" ]; then echo "$MNJ_DAY"; return; fi
  shifted=$(date -d '-8 hours' +%Y%m%d 2>/dev/null) || shifted=$(date +%Y%m%d)
  if [ "$shifted" -ge 20260627 ]; then echo 2; else echo 1; fi
}

DAY=$(pick_day "$1")
DIR="$FRAMES_DIR/day$DAY"

# Quiet the kernel console + hide cursor so nothing draws over the image.
dmesg -n 1 2>/dev/null
setterm -cursor off -blank 0 -powerdown 0 2>/dev/null

# Show the frames (fbi stays running on the console, default loops).
fbi -d /dev/fb0 -T 1 -a --noverbose "$DIR"/frame*.png &
FBI_PID=$!

# Let fbi grab the console and draw the first frame.
sleep 3

cleanup() { kill "$FBI_PID" 2>/dev/null; }
trap cleanup INT TERM EXIT

# Drive the fast neon flicker by injecting 'j' (next image) into the console.
# Runs as long as fbi lives; if fbi dies, the driver exits and so do we.
exec python3 "$TOOLS_DIR/flicker.py" "$TTY" "$FLICKER_S"
