#!/bin/sh
# MNJ 2026 framebuffer kiosk.
# Picks the day's frame set by date (8h backshift so a party running past
# midnight still counts as the night it started on) and shows the frames on
# the console framebuffer with fbi, cycling them to fake the neon blink.
#
#   Fri Jun 26 2026 -> day1
#   Sat Jun 27 2026 -> day2
# Override: pass 1 or 2 as $1, or set MNJ_DAY=1|2 in the environment.

FRAMES_DIR="${MNJ_FRAMES:-/home/mos/kiosk_frames}"
CYCLE="${MNJ_CYCLE:-1}"   # fbi seconds per frame (integer; min 1)

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

# Never return to a shell prompt: if fbi ever exits, clear and relaunch.
# fbi cycles the frames on its own timer (-t), looping by default.
while :; do
  fbi -d /dev/fb0 -T 1 -a --noverbose -t "$CYCLE" "$DIR"/frame*.png
  clear 2>/dev/null
  sleep 1
done
